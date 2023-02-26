# Poetry Toolkit

**deployment coming soon!**

*contact the developer:* [June Balter -- LinkedIn](https://www.linkedin.com/in/june-balter/)

**Demo Video:** [YouTube](https://www.youtube.com/watch?v=i6cDlsd1Lxk)

Poetry Toolkit is an app for people who like poems. The goal is to inspire users to read more and write more by making accessible and approachable tools for English-language poets.

Using the [PoetryDB](https://poetrydb.org/index.html) API, as well as our built-in database, users can view centuries of poetry and search for authors or titles they like. They can also respond to poetry prompts or create their own to inspire other users. Users can also create poem mashups by randomly mixing and matching lines from existing works. Users can save their prompt responses and their favorite mashups to their profile and choose to share them with other users.

![Poetry Toolkit front page](/README/Front%20Page.png)
![Poetry Toolkit poems page](/README/Poems%20bookmark%20alert.png)
![Poetry Toolkit prompts page](/README/Prompts.png)
![Poetry Toolkit mashups page](/README/Mashups.png)
![Poetry Toolkit user profile page](/README/User%20Profile.png)


# Tech Stack:
- Python, Flask, Jinja 
- Javascript (AJAX, React), CSS, HTML, Bootstrap
- PostgreSQL, SQLAlchemy
- PoetryDB API


# Development Diary:

### Day 1, 12/18/22: Brainstorming project ideas:
- music-related:
    - basic synthesizer:
        - produce soundwaves
        - alter pitch
        - change filter/effects
        - learn about basic synthesizer functionality
        - basic FL type daw:
        - 4-8 channels
        - 4 melody/bass
        - 4 percussion
        - looping
        - adjust BPM
        - adjust time signature
        - GUI to enter in beats on a grid
        - just drums? melody interface different?
- poetry-related
    - prompt-generator:
        - user inputs that affect outcome
        - questions?
    - writing collaboration platform:
        - connect users with creative ways to limit/inspire collaboration (not just a blank page)
        - would require messaging/internet functionality
    - line-break machine:
        - fucks up your lines for you to make your poems better!
        might be too simple of a project?
- other:
    - game of some sort
        - more brainstorming needed

### Day 2 12/20/22 - discussing with Trew, advising #1:
- poetry APIs exist
- web sockets are challenging
- search feature - key word, database building (to store poetry)
- multiple users working on the same doc
- will I be excited for 4 weeks straight? something joyful
- save presets for synthesizer
- private/public database options, searchable presets
- include React in project (might increase hireability)

### Day 3 1/5/23
- lol i never wrote anything on this day, why didn’t I delete this header? 🤷 (2/19/2023)

### Day 4 1/10/23
- MVP outlines:
	- Synthesizer MVP:
        - user log in
        - simple inputs to modify sound (tone.js framework)
        - be able to save settings to database and load / share
        - randomized settings for inspiration
	- Nice to haves:
        - more robust input/sequencing options
        - multi-user collaboration
        - public/private database to search for presets
        - dynamic mapping of users?
	- Poetry MVP:
        - poetryDB framework
        - prompt-generator
        - line-break machine (enter poetry, returns new line breaks)
        - use poetryDB to generate poems for inspiration
	- Nice to haves:
        - user inputs to affect prompt-generator
        - database to store/share poetry
        - collaboration tools for multiple users
        - dynamic mapping of users?
	- Bonus:
		- for any project, nice to have:
            - avatar generation/customization via classes
            - unlock upgrades by interacting somehow?
            - stock images - sprout to flower, based on number of interactions?

            - data visualization of lyrics
            - break down poems by particular words and phrases, dynamic mapping

### Day 5 1/17/2023
Visualized poetry/synth sites as flow charts

Every day, try to make a note:
What did you struggle with?
Did you figure something out?
Did you fail to figure something out?
Did you make hard trade-offs?
What did you study?
What did you learn?
How do you work?
What do you need?

## Actual Project Time:
### Day 6 1/30/2022:
- Was sick last week so didn’t keep this diary

### Day 7 1/31/2023:
Commits today:
- “we can now load user comments and saved poems, as well as user responses and saved prompts, on new savedpoems / savedprompts templates” 5:15PM
    - sending poem/prompt id via post request from submit buttons that display this id # on the user profile - feels like there must be a better way to handle this, or at least mask the id # (maybe this can be resolved via React when/if I get to that?
- "you can now edit and save edits to the database for responses and comments by opening them from the user profile" 8:52PM
    - Trew helped me solve the previous problem using "<input type=”hidden”>"
    - next steps for tomorrow is to investigate how to implement user profile using React
### Day 8 2/1/2023:
- "userprofiletest route to assess building user profile with React was successful" ~7:30PM (commited 11AM 2/2)
    - successfully recreated the userprofile page using react, links appear to be populating and work as expected (identical to previous version)
    - i think this will be useful for styling and good practice for wrapping my head around React - will have to think if there are any other useful and more dynamic ways to implement React into the app
### Day 9 2/2/2023:
- added search functionality for author, title, and line count (5:45 PM)
- mashup route is working, need to adddd more functionality for title and author (8:15 PM)
### Day 10 2/3/2023:
- added keyword search for lines/body on poem page (2:10 PM)
- "added title and author generation for mashups, tweaked value input to number, added easter eggs for poems of certain line lengths" (3:34PM)
- “phew got mashups to saved to the database and they now load on the userprofiletest jsx page as well!” (7:06 PM)
### Day 11 2/4/2023:
- rerouted user profile to the React version (12:38 PM)
### Day 12 2/6/2023:
- “added checkboxes to u user profile for updating public status of prompts/mashups (non-functional)” (6:06) PM
   - these are “read-only” because of the way React renders things - need to research out to get these to work and build routes for updating each
- “working template for viewing saved mashups” (6:48 PM)
   - no JS at this time
- “tweaked display for userprofile (links changed to text, button text updated)” (7:07 PM)
   - minor display tweaks
- “added bootstrap accordion to prompt responses on user page, not sure if this is totally feasible with the way boostrap appears to be structured here” (7:42 PM)
   - bootstrap appears to have pre-structured names such as “collapseOne” “collapseTwo” etc. it’s unclear if/how I can get the for loop for the .jsx file to render this correctly, otherwise all accordions response to all interactions
### Day 13 2/7/2023:
- "added bootstrap accordion to just the headers in the user profile template, will have to remove them from the jsx - this is more appropriate for now" (1:45 PM)
- "started templates for public prompt and mashup display pages, mashup html and jsx working" (committed Wednesday 2:07 PM)
### Day 14 2/8/2023:
- “public user prompts and mashups pages s are both functional” (4:29 PM)
- “pufixed styling of user profile page and search pages for readability” (5:04 PM)
- “password hashing added” (6:11 PM)
- “add prompt template created, need to add functionality” (7:26 PM)
- “add prompt page is now functional” (7:58 PM)
### Day 15 2/9/2023:
- “updated mashups route to prevent saving mashups before generation” (11:53 AM)
- "finally got the checkboxes working on the userprofile page - needed to break out the prompt and mashup items into individual compenents instead of instantiating a single component as a list, allowing for useState to control checkbox - still need to get the update button routing working" (7:43 PM)
### Day 16 2/10/2023:
- mashup and prompt cards are now matching - DOMException error for querySelector for the update button IDs needs to be addressed (11:41 AM)
- minor formatting update to saved poem template (11:54 AM)
- "update public/private functionality on user profile is now working" (2:47 PM)
    - bug where the checkmarks for mashups appear to default to true even when boolean is false in the database (correctly not showing up in public mashup list) - this is not happening in the prompts section
- “added routing and templates for deactivating a user account and reactivating it with successful login” (6:59 PM)
### Day 17 2/11/2023:
- "created logged in decorator" (12:37 AM)
    - decorators are neat, need to dig in more to learn how to use them
### Day 18 2/13/2023:
- "started a utilities module file and did some debugging on server.py" (8:10 PM)
### Day 19 2/14/2023:
- added bootstrap to the homepage
### Day 20 2/15/2023:
- "added accordion menu to optional inputs for poem search" (2:22 PM)
- "oops i did some styling" (3:08 PM)
- began adding testing in test_server file to check routing success (8:22 PM)
- added new bootstrap to the homepage, added a function to make multiple API calls for mashups to increase diversity of sources especially for smaller linecounts, minor styling (10:01 PM)
- fixed seed database bug, minor styling to user page (10:29 PM)
### Day 21 2/16/2023:
- "added logged_in_JSON decorator, generally cleaning up code and checking for bugs" (3:44 PM)
- "added more testing to test_server, cleaned up a couple of minor bugs" (5:55 PM)
- "bug fixing, tightening up code, testing purple class styling" (7:31 PM)
### Day 22 2/17/2023:
- "sorted out the styling so that user profile cards, public mashup cards, and public prompts cards now appear in responsive rows. also added page-header styling" (2:52 PM)
    - so many nested divs makes finding the right place to adjust bootstrap / CSS elements tricky with React, careful attention to id/class names is needed in the future
- "moved payload functionality for user inputs to utils.py" (5:14 PM)
- "added testing for server and utils" (7:04 PM)
### Day 23 2/19/2023:
- “lots of bootstrap/css adjusting - mostly making cards more responsive and uniformly sized regardless of content - also some subtle updates to border formatting etc.” (3:37 PM)
- "updates to test_utils and test_server to increase coverage of json routes" (6:41 PM)
- "combined test_server and test_utils into one file, tests.py, for more accurate coverage reporting" (7:00 PM)
- “"tweaked tests.py" (7:08 PM)
### Day 24 2/20/2023:
- “added mock API call for random poem to tests.py” (11:53 AM)
- “more styling tweaks - primarily, getting navbar dropdowns to appear beneath their appropriate headers” (2:42 PM)
- “updated a lot of styling - fixed some div layering for bootstrap containers, chose a new font Lora for the page, added an SVG icon to the navbar, adjusted the opacity of the background image, other small touches as well” (7:56 PM)
### Day 25 2/21/2023:
- "added hover functionality to mashup lines so that original authors/titles appear next to the lines when hovered" (11:51 AM)
- “fixed mashup issue where occasionally empty lines would be included" (11:57 AM)
- “added italics to h3 and drop-shadow to interactable buttons (excluding ? buttons)” (1:13 PM)
- “added more flask testing in tests.py” (6:59 PM)
### Day 26 2/22/2023:
- "added more flask testing for more routes in tests.py" (1:54 PM)
- “more testing, 50% server.py coverage, 77% project coverage - updated styling on card buttons in user profile” (6:33 PM)
- “updated styling for saved poems page and saved prompts page to be in line with the rest of the site” (6:55 PM)
- "fixed the public checkbox bug on the mashups section of the user profile and cleaned up some spacing issues on the public prompts and mashups pages" (7:32 PM)
- "got the username-corner route working!" (7:43 PM)
### Day 27 2/23/2023:
- “nothing changed, just getting up to date” (2:35 PM)
- “added favicon” (7:22 PM)
### Day 28 2/26/2023:
- “created a README file” (1:33 PM)
- “added this diary to the README”
