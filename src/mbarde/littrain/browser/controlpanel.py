# -*- coding: utf-8 -*-
from mbarde.littrain import _
from plone import api
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from z3c.form import button
from zope import schema
from zope.interface import Interface

import logging


class ILitTrainControlPanelView(Interface):

    books_folder = schema.TextLine(
        title=_(u'Books folder'),
        description=_(u'Folder where books are stored.'),  # noqa: E501
        required=True,
    )


class LitTrainControlPanelForm(RegistryEditForm):
    schema = ILitTrainControlPanelView
    schema_prefix = 'littrain'
    label = u'LitTrain Settings'

    @button.buttonAndHandler(_(u'Count stored lemmas'))
    def handleCount(self, action):
        brains = api.content.find(portal_type='Lemma')
        api.portal.show_message(
            message=_(u'There are ${successCount} lemmas',
                      mapping={u'successCount': len(brains)}),
            request=self.request, type='info')

    @button.buttonAndHandler(_(u'Show undefined lemmas'))
    def handleFindUndefined(self, action):
        undefinedLemmas = []
        brains = api.content.find(portal_type='Lemma')
        for brain in brains:
            lemma = brain.getObject()
            if len(lemma.definitions) == 0:
                undefinedLemmas.append(lemma.title)

        message = ', '.join(undefinedLemmas)
        api.portal.show_message(
            message=message, request=self.request, type='info')

    @button.buttonAndHandler(_(u'Update all lemmas'))
    def handleUpdateAll(self, action):
        brains = api.content.find(portal_type='Lemma')
        brainCount = len(brains)
        logging.info(u'Found {0} lemmas to update ...'.format(str(brainCount)))

        counter = 0
        reportInterval = 50
        for brain in brains:
            lemma = brain.getObject()
            lemma.updateDefinitions()
            counter += 1
            if counter % reportInterval == 0:  # noqa: S001
                percentage = int(float(counter) / float(brainCount) * 100)
                logging.info(u'Updated {0}% of all lemmas'.format(percentage))

        logging.info(u'Successfully updated {0} lemmas'.format(str(counter)))

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleSave(self, action):
        errorMsg = False
        data, errors = self.extractData()

        if 'books_folder' in data:
            booksPath = data['books_folder']
            portal = api.portal.get()
            try:
                folder = portal.restrictedTraverse(str(booksPath))
                if folder.portal_type != 'Folder':
                    errorMsg = _(u'Item at this location is not a folder!')
            except KeyError:
                errorMsg = _(u'Folder does not exist at this location!')

            if errorMsg:
                api.portal.show_message(
                    errorMsg, request=self.request, type='error')

        if errors or errorMsg:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)
        api.portal.show_message(
            message=_(u'Changes saved.'),
            request=self.request, type='info')
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        api.portal.show_message(
            message=_(u'Changes canceled.'),
            request=self.request, type='info')
        self.request.response.redirect(u'{0}/{1}'.format(
            api.portal.get().absolute_url(),
            self.control_panel_view,
        ))


LitTrainControlPanelView = layout.wrap_form(
    LitTrainControlPanelForm, ControlPanelFormWrapper)
