# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s mbarde.littrain -t test_chapter.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src mbarde.littrain.testing.MBARDE_LITTRAIN_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/mbarde/littrain/tests/robot/test_chapter.robot
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

Scenario: As a site administrator I can add a Chapter
  Given a logged-in site administrator
    and an add Book form
   When I type 'My Chapter' into the title field
    and I submit the form
   Then a Chapter with the title 'My Chapter' has been created

Scenario: As a site administrator I can view a Chapter
  Given a logged-in site administrator
    and a Chapter 'My Chapter'
   When I go to the Chapter view
   Then I can see the Chapter title 'My Chapter'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Book form
  Go To  ${PLONE_URL}/++add++Book

a Chapter 'My Chapter'
  Create content  type=Book  id=my-chapter  title=My Chapter

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Chapter view
  Go To  ${PLONE_URL}/my-chapter
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Chapter with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Chapter title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
