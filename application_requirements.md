# Haunted Asylum Functional Requirements

# Overview

This document provides a brief overview of the features, functions and components that are required in the “Haunted Asylum” Vue3 based decision making horror game. The game features a linear narrative told through a series of videos, cinematics,  played within the application between “checkpoints”. Checkpoints are interfaces placed between cinematics, where the player must make a decision between two choices. At every checkpoint, one decision will progress the narrative and game, while the other will lead to a game over state and take the player back to the start. Making the correct decision at every checkpoint will allow the player to reach the end of the game and fulfill the win condition.

*Note:* Audio elements in the game will be included later, in sections where audio assets are mentioned, please write placeholder code. 

# Visual Style

User Interface elements in the game, such as buttons and the title text should be dark and gothic in style, primarily featuring dark greys, reds, and black.

# Pages

This section lists each page required in the application, and the components and functionalities on each of these pages.

## Start Page

The Start Page is the first page of the application on start. 

1. Background: A full screen image set as the background   
2. Start Button: A button located in the bottom center that plays the start cinematic and initiates the game session

## Checkpoint Page

The Checkpoint Page appears between cinematics, whenever a choice is available for the player to make. The game will consist of three checkpoints, and the contents of the page will vary based on which of the three checkpoints the current game session has progressed to. However, the layout and component types in the page will remain the same at each checkpoint. 

1. Choice Buttons: Each checkpoint will feature two choices for the player to choose from, as such there will be two buttons with text describing the choices. The text content will change depending on which checkpoint the player is currently at. Clicking on one of the two buttons will progress the narrative and redirect to the cinematic player to play the corresponding video.  
2. Background: Image reflecting the narrative checkpoint where the player is currently at.

## Cinematic Player

The cinematic player is not an interactive page, it is a state in the application when narrative related videos are being played. Whenever a cinematic video is being played, there are no buttons or components for the player to interact with. Cinematic videos will start playing automatically. 

*Note:* put placeholders for the mp4 files in the cinematic player

## Game Over Page

The Game Over Page appears after the player clicks a choice button that leads to an immediate game failure, and the corresponding cinematic is played by the Cinematic Player. 

1. Game Over Text: Red words at the center of the screen reading “Game Over”  
2. Return to Home button: A button that on click redirects the player to the start page and resets the game progression

## True Ending Page

The Game Over Page appears after the player successfully passes the third checkpoint. It briefly displays the words "True Ending" before automatically redirecting the player to the Start Page.

1. True Ending Text: Red words at the center of the screen reading “Game Over”  