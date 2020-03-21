# -*- coding: utf-8 -*-
from plone import api

import json


LEARNED_LEMMAS_PROPERTY_NAME = 'learned_lemmas'


def getUsersLearnedLemmas(user=None):
    if user is None:
        user = api.user.get_current()
    learnedStr = user.getProperty(LEARNED_LEMMAS_PROPERTY_NAME)

    try:
        learned = json.loads(learnedStr)
    except json.decoder.JSONDecodeError:
        learned = []
    if not isinstance(learned, list):
        learned = []

    return learned


def addToUsersLearnedLemmas(lemma, user=None):
    if user is None:
        user = api.user.get_current()

    learnedLemmas = getUsersLearnedLemmas(user)
    uuid = api.content.get_uuid(lemma)
    if uuid in learnedLemmas:
        return
    learnedLemmas.append(uuid)

    llStr = json.dumps(learnedLemmas)
    user.setMemberProperties(
        mapping={LEARNED_LEMMAS_PROPERTY_NAME: llStr})


def deleteFromUsersLearnedLemmas(lemma, user=None):
    if user is None:
        user = api.user.get_current()

    learnedLemmas = getUsersLearnedLemmas(user)
    uuid = api.content.get_uuid(lemma)
    if uuid not in learnedLemmas:
        return
    learnedLemmas.remove(uuid)

    llStr = json.dumps(learnedLemmas)
    user.setMemberProperties(
        mapping={LEARNED_LEMMAS_PROPERTY_NAME: llStr})


def isLemmaLearnedByUser(lemma, user=None):
    if user is None:
        user = api.user.get_current()

    learnedLemmas = getUsersLearnedLemmas(user)
    uuid = api.content.get_uuid(lemma)
    return uuid in learnedLemmas
