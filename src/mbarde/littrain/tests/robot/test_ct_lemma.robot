# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s mbarde.littrain -t test_lemma.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src mbarde.littrain.testing.MBARDE_LITTRAIN_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/mbarde/littrain/tests/robot/test_lemma.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Lemma
  Given a logged-in site administrator
    and an add Lemma form
   When I type 'My Lemma' into the title field
    and I submit the form
   Then a Lemma with the title 'My Lemma' has been created

Scenario: As a site administrator I can view a Lemma
  Given a logged-in site administrator
    and a Lemma 'My Lemma'
   When I go to the Lemma view
   Then I can see the Lemma title 'My Lemma'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Lemma form
  Go To  ${PLONE_URL}/++add++Lemma

a Lemma 'My Lemma'
  Create content  type=Lemma  id=my-lemma  title=My Lemma

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Lemma view
  Go To  ${PLONE_URL}/my-lemma
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Lemma with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Lemma title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
