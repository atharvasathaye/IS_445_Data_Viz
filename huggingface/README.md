# Instructions for this assignment

# Is this file opened with (Right click on the file) ->Open Preview?

It should look like:

![readme opened with preview](readme_imgs/openPreview.png)

## Step 1: Organize your VSCode workspace -- Terminal

We'll need the Terminal app to clone a template HuggingFace Spaces Repository.

![pull up on the bottom "line" of the VSCode instance to get the Terminal](readme_imgs/pull_up_terminal.gif)

Alternatively, you can use `View -> Terminal` to see the Terminal.

![view terminal option](readme_imgs/view_terminal.png)


## Step 2: Create a HuggingFace Account (if you haven't already)

Go to [huggingface.co](https://huggingface.co/) and click on "Sign Up":

![huggingface.co](readme_imgs/huggingfaceLanding.png)

Once signed up, you should be taken to your homepage.  Mine looks like this (but note, if this is your first time signing in, you likely won't have any project spaces, so there will likely be less stuff on your page):

![jnaiman huggingface](readme_imgs/whathflookslike.png)


## Step 3: Duplicate the IS445 Demo Space

**Step 3.1:** Head to the template webpage: [https://huggingface.co/spaces/jnaiman/is445_demo](https://huggingface.co/spaces/jnaiman/is445_demo).

**Step 3.2:** Click on "Duplicate this Space":

![duplicate the huggingface space](readme_imgs/duplicateSpace_p1.png)

**Step 3.3:** Duplicate the Space with your username:

![change user name to duplicate space](readme_imgs/duplicateSpace_p2.png)

*Be sure to check the following:*
1. Is the username your HuggingFace username?
2. Is the Space name "is445_demo"?
3. Have you set the "Visibility" to `Public`?

## Step 4: Wait for the IS445 Demo Space to "Build"

Once duplicated, you will see it building, it will start with just one line:

![](readme_imgs/build_start.png)

This tells us our build is "queuing" -- *note this can take a bit so be patient!* If it is queuing for over an hour, you can try to do a "Factory Rebuild" as discussed [here](https://discuss.huggingface.co/t/app-in-spaces-takes-forever-in-building/38940) and [here](https://discuss.huggingface.co/t/can-i-force-rebuild-a-huggingface-space/18419).

Once building it should have output like:

![](readme_imgs/building_during.png)

And then it will switch to the "Container" tab before launching your Space:

![](readme_imgs/building_success.png)

If you click on your Space behind this you should see your interactive web-app:

![](readme_imgs/built_space.png)


## Step 5: Set up a token to use with HuggingFace

Next you will create an [access token for your HuggingFace account](https://huggingface.co/docs/hub/en/security-tokens). 

**Step 5.1:** Navigate to the "Access Tokens" page from "Settings" under your username:

![](readme_imgs/accesskey_p1.png)

**Step 5.2:** Create a new finegrained token with read/write access to your personal repositories.

First, click on the "Create new token" button on this page.  

Then select a Finegrained token with read/write access to your personal repos:

![](readme_imgs/accesskey_p2.png)

**Step 5.3:** Generate the Token and *save it somewhere safe* 
1. Click on `Create Token` at the bottom of the current page
2. *Save the token string somewhere safe!* We will be using this token throughout this class.

## Step 6: Clone the repository

**Step 6.1:** Click on the "Clone repository" button:

![](readme_imgs/clone_the_repo.png)

**Step 6.2:** Copy the "git clone" command:

![](readme_imgs/gitclone_hf.png)

**Step 6.3:** Copy the "git clone" command into the Terminal and run to clone:

![](readme_imgs/gitclone_workspace.png)

Now you should see a directory called `is445_demo` in the VSCode interface.

## Step 7: Run the Streamlit App Locally

**Step 7.1:** Run the streamlit app by `cd`ing into the `is445_demo` directory and running the app with `streamlit run app.py`:

![](readme_imgs/run_streamlit_app.png)

**Step 7.2:** Open your locally running app in the browser by either 
1. clicking on "Open in Browser", or
2. opening the port in the "Simple Browser" like we did in class (and shown below)

![](readme_imgs/portForwardOpen.png)

## Step 8: Open the `app.py` file and update a few parameters

Open up the `app.py` file by double clicking on it in the left-hand side bar in VSCode.

Make the following substitutions:
1. Replace the "st.title" (My First Streamlit App) with "Streamlit App for IS445: ID27773" in the file called "is445_demo/app.py"
2. Replace the x-axis "title" (Date) with "Date (Month Year)" in the file called "is445_demo/app.py"
3. Replace the chart title (Seattle Weather: 2012-2015) with "Seattle Weather - 2015 to 2023" in the file called "is445_demo/app.py"
4. Replace *JUST* the URL in "st.text" (https://huggingface.co/spaces/jnaiman/is445_demo) with "[the URL for your instance]." in the file called "is445_demo/app.py"
5. Replace the "title" (Example for IS445) with "My IS445 Example ID27773" in the file called "is445_demo/README.md"


## Step 9: Push your changes to your HuggingFace Repository

All of the following steps are done in the `Terminal` part of VSCode (after stopping the running of streamlit with "CTRL + c"):

**Step 9.1:** Add all changes

```
git add -A
```

**Step 9.2:** Commit the changes

```
git commit -m "uploading changes to template"
```

**Step 9.3:** Push the changes

```
git push
```

**You will need to enter your username and token you saved here!** 

**NOTE:** You may also see that you need to enter your credentials in the terminal (you might have had to do this in Lab \#4):

![enter huggingface credentials](readme_imgs/credentials_gitconfig.png)

Follow the instructions that print out and user your HuggingFace email and username.

## Step 10: Wait for your App to build -- your URL is automatically parsed and checked

Once you have pushed your changes, you need to wait for your App to build (see **Step 4**).

<!-- 
Then, submit the URL for your app in the main "grading" page for this assignment and hit "Save & Grade".

For example, I would submit the URL:

```
https://huggingface.co/spaces/jnaiman/is445_demo
```
-->


