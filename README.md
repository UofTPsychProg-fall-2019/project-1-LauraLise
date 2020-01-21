# project-1-LauraLise

############## DESCRIPTION OF MY EXPERIMENT ############################

    # I have created a verbal N-back task using Psychopy, which I hope to use for an fMRI study.
    # The 1-, 2-, and 3-back versions of the task will be used
    # I initially was set on using E-prime to develop my task, however, it was not as user friendly as I anticipated 
    # Furthermore, I like coding my experiments rather than using a GUI builder, making the Psychopy coder a logical choice 

    # Before doing the experiment, participants will practice at least one block of the 1-back, 2-back and 3-back task 
    # During practice, participants will receive feedback on their performance, however, they will not receive feedback during the actual       experiment 
    # They can choose to repeat practice if they are having difficulty understanding the task

    # Participants will need to indicate with a button press if the current stimulus is a target or non-target stimulus.
    # The f key will be used for non-targets and the j key will be used for targets
    # Accuracy and reaction time of each response will be recorded
    # A block will consist of 12 trials. Below is the breakdown of the trial types for each version of the task: 
        # 1-back: 3 targets, 9 non-targets 
        # 2-back: 3 targets, 3 lures, 6 non-targets 
        # 3-back: 3 targets, 3 lures, 6 non-targets 
    
    # Each letter stimulus will be presented for 0.5 seconds, with a fixed ISI of 1.5 seconds (during which a fixation cross will be on         screen) 
    # Two output files will be generated - one output file for their practice session and another for the experiment session, which are         stored in separate folders
    # During the experiment, participants will complete four 1-back blocks, seven 2-back blocks, and seven 3-back blocks 
    # The order in which they complete the blocks will be randomzied 
    # I have created several CSV files with the letter sequence participants will be shown for each block 
 



# To run this experiment, you need to create two folders called, "PRACTICE_data" and "TASK_data" in the same directory as the psychopy experiment file (the data from the practice and task will save in these folders). Also, when running this experiment, you will need to press 1 to advance from the practice to the test.
