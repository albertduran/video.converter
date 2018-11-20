# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone.app.layout.navigation.root import getNavigationRootObject
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.deprecation.deprecation import deprecate
from zope.interface import implementer
from zope.viewlet.interfaces import IViewlet


@implementer(IViewlet)
class ViewletBase(BrowserView):
    """ Base class with common functions for link viewlets.
    """

    def __init__(self, context, request, view, manager=None):
        super(ViewletBase, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

    @property
    @deprecate("Use site_url instead. " +
               "ViewletBase.portal_url will be removed in Plone 4")
    def portal_url(self):
        return self.site_url

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.navigation_root_url = self.portal_state.navigation_root_url()
        self.navigation_root_title = self.portal_state.navigation_root_title()

        context = aq_inner(self.context)

        context_state = getMultiAdapter((context, self.request),
                                        name=u'plone_context_state')

        user_actions = context_state.actions('user')
        self.user_actions = []
        for action in user_actions:
            info = {
                'title': action['title'],
                'href': action['url'],
                'id': 'personaltools-{}'.format(action['id']),
                'target': action.get('link_target', None),
            }
            modal = action.get('modal')
            if modal:
                info['class'] = 'pat-plone-modal'
                info['data-pat-plone-modal'] = modal
            self.user_actions.append(info)

        self.anonymous = self.portal_state.anonymous()

        if not self.anonymous:
            member = self.portal_state.member()
            userid = member.getId()

            self.homelink_url = "%s/useractions" % self.navigation_root_url

            membership = getToolByName(context, 'portal_membership')
            member_info = membership.getMemberInfo(userid)
            # member_info is None if there's no Plone user object, as when
            # using OpenID.
            if member_info:
                fullname = member_info.get('fullname', '')
            else:
                fullname = None
            if fullname:
                self.user_name = fullname
            else:
                self.user_name = userid

    def render(self):
        # defer to index method, because that's what gets overridden by the
        # template ZCML attribute
        return self.index()

    def index(self):
        raise NotImplementedError(
            '`index` method must be implemented by subclass.')


class GlobalSectionsViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlets_templates/sections.pt')

    def update(self):
        super(GlobalSectionsViewlet, self).update()
        context = aq_inner(self.context)
        portal_tabs_view = getMultiAdapter((context, self.request),
                                           name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs()

        self.selected_tabs = self.selectedTabs(portal_tabs=self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']

    def selectedTabs(self, default_tab='index_html', portal_tabs=()):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        plone_url = getNavigationRootObject(
            self.context, portal).absolute_url()
        plone_url_len = len(plone_url)
        request = self.request
        valid_actions = []

        url = request['URL']
        path = url[plone_url_len:]
        path_list = path.split('/')
        if len(path_list) <= 1:
            return {'portal': default_tab}

        for action in portal_tabs:
            if not action['url'].startswith(plone_url):
                # In this case the action url is an external link. Then, we
                # avoid issues (bad portal_tab selection) continuing with next
                # action.
                continue
            action_path = action['url'][plone_url_len:]
            if not action_path.startswith('/'):
                action_path = '/' + action_path
            action_path_list = action_path.split('/')
            if action_path_list[1] == path_list[1]:
                # Make a list of the action ids, along with the path length
                # for choosing the longest (most relevant) path.
                valid_actions.append((len(action_path_list), action['id']))

        # Sort by path length, the longest matching path wins
        valid_actions.sort()
        if valid_actions:
            return {'portal': valid_actions[-1][1]}

        return {'portal': default_tab}
