# DLM Usage

The DL Manager is a complex system with a variety of components that together make up for its main workflow. Below are the steps to hosting DL Manager on your own AWS DeepLens!

## Connecting to your DeepLens

Follow the [step by step tutorial by AWS here](https://docs.aws.amazon.com/deeplens/latest/dg/deeplens-getting-started-register.html) to register and setup ur DeepLens device. Make sure to enable SSH when you reach the `deeplens.amazon.net` site for device configuration [here](https://docs.aws.amazon.com/deeplens/latest/dg/deeplens-getting-started-set-up.html).

## SSH into your DeepLens

1) Log into the [AWS Management Console](https://aws.amazon.com)
2) Go into the `AWS DeepLens` service
3) Click on your registered AWS Deeplens's device name

![Example registered device](/documentation/registeredDevice.png)

4) Under the `Device details` section, copy the `IP address` into your clipboard; this will be necessary for SSHing into the DeepLens.
5) Open up your Terminal
6) Type in the following: `ssh aws_cam@<YOUR DEEPLENS IP ADDRESS>`, where `<YOUR DEEPLENS IP ADDRESS>` will be replaced by the IP address of the DeepLens that you copied earlier.
7) Enter your set DeepLens password when the prompt comes up

## Getting DL Manager on your DeepLens

1) Run the following in the terminal window when you have successfully SSHed in:

```zsh
mkdir Manager && cd Manager && git clone https://github.com/Prakhar896/DL-Manager
```

> The above command will make a directory called `Manager` in the home directory of the `aws_cam` account. It then clones the DeepLens Manager Github Repository via `git clone ...`

2) Change directory into the cloned folder: `cd DL-Manager`

> To see what the expected output of step 1 and 2 should be, [view a short clip here](/documentation/gettingDLManagerOutput.mov)

## Setting up DL Manager

Out of the box, DL Manager comes with a safe boot feature that is turned on by default, which ensures that the system environment is appropriate and all necessary environment variables are present. If you try to run the `main.py` script without setting up, safe boot will throw you an error, with more information on what was wrong in the environment.

Below are a few steps to setup DL Manager (considering you are using your Terminal and do not have access to the DeepLens's Ubuntu GUI):

1) Make a `.env` file by runnning `touch .env`
2) Use the in-built Terminal file editor to edit (the `nano` editor can be quite daunting and nonintuitive and hence I have made a complete section below on how to add in the environment variables from just the Terminal)

---
### Using Nano to write to .env file

[Nano](https://help.ubuntu.com/community/Nano#:~:text=GNU%20nano%20is%20a%20simple,writing%20short%20plain%20text%20files.&text=Nano%20can%20be%20used%20in,or%20at%20the%20system%20console.) is a in-built command line text editor that one can use to edit files.

FOLLOW THE STEPS BELOW EXTREMELY CLOSELY:

1) Run `nano .env` into the command line. This will clear your terminal window and bring up a text editor. It should say `File: .env` at the top.

> You need 3 environment variables for DL Manager to boot - `deepLensPwd`, `DLAccessCode`, `RuntimePort`

2) Make an environment variable called `deepLensPwd` and set it to whatever you would like to (ideally it should be the password for your DeepLens' `aws_cam` account) and you will use this to login to the system later

E.g:
```
deepLensPwd=Password12345
```

3) Make another environment variable called `DLAccessCode` (this is an internal access code part of the authorisation layer, you don't need to worry too much about it) and set it to `AWSDL@Prakh!6070`

E.g:
```
deepLensPwd=Password12345
DLAccessCode=AWSDL@Prakh!6070
```

4) Finally, make an environment variable called `RuntimePort`, which will be the port used when the web server is being run and set it to anything higher than 8800, for e.g 8890 (this is due to what ports the DeepLens already uses for its own purposes)

E.g:
```
deepLensPwd=Password12345
DLAccessCode=AWSDL@Prakh!6070
RuntimePort=8890
```

5) After you are done making these variables, follow these keyboard shortcuts to save and exit the Nano editor:

```
Control + O (the letter O), press enter, Control + X
```

The last step should bring you back to the normal command line, with the `.env` file full of three environment variables.

To see the ideal output for making an editing a .env file, [watch this short clip](/documentation/editingENVFileOutput.mov)

---

3) Install all the required libraries using `pip install -r requirements.txt`
4) Finally, run the server by running `python main.py`. You should see safe boot being successful and the server starting and serving content on the `RuntimePort` you chose.

> If safe boot encounters an error, read the error it provides and go back through this tutorial to check where you went wrong in setting up DL Manager

5) Lastly, in order for this web server to be acccessed by any computer that is on the network that the DeepLens is connected to, you will need to run `sudo ufw allow <RUNTIME PORT>`, where `<RUNTIME PORT>` will be replaced by the `RuntimePort` that you keyed into the `.env` file [earlier](#using-nano-to-write-to-.env-file).

> The above step tells DeepLens' firewall to allow the port you chose to be opened up to all devices on your network.

If all goes well, you can now access the DeepLens without using SSH using the DL Manager by simply opening up a browser on any computer thats on the same WiFi as the DeepLens and entering the URL: `http://<YOUR DEEPLENS IP ADDRESS>:<RUNTIME PORT>`, for e.g `http://192.168.84.74:8890/`

### SSH Code feature

The DLM automatically generates a file called `sshCode.md` under the folder `supportFiles` which is under the root DLM folder. This file is helpful for the user, as it serves to be a quick manner of copying-and-pasting SSH code into your terminal to get access to the DeepLens.

When the server first runs, the DLM sets this to a template which you can update yourself by editing the `sshCode.md` file with the correct DeepLens IP address and the DeepLens `aws_cam` account password.

This change will be reflected in the web server when you click on the `SSH Code` link in the homepage of the DLM (which comes up after you login to the system.)

## Running DL Manager 24/7

This section assumes that you have the latest version of the [Node Package Manager (npm) installed.](https://npmjs.com)

1) Install a package called `forever` globally by running `npm i -g forever` (the `-g` tag makes it globally available)
2) Ensure that you are in the DL Manager directory and run `forever start -c python main.py`

This should start running the manager in the background and will keep it running even if you close the SSH session.

> If you would like to stop the server, simply run `forever stop main.py`

© 2022 Prakhar Trivedi