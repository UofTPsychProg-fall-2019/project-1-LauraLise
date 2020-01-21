
############## DESCRIPTION OF MY EXPERIMENT ############################

# I have created a verbal N-back task using Psychopy, which I hope to use for an fMRI study.
# The 1-, 2-, and 3-back versions of the task will be used
# I initially was set on using E-prime to develop my task, however, it was not as user friendly as I anticipated 
# Furthermore, I like coding my experiments rather than using a GUI builder, making the Psychopy coder a logical choice 

# Before doing the experiment, participants will practice at least one block of the 1-back, 2-back and 3-back task 
# During practice, participants will receive feedback on their performance, however, they will not receive feedback during the actual experiment 
# They can choose to repeat practice if they are having difficulty understanding the task

# Participants will need to indicate with a button press if the current stimulus is a target or non-target stimulus.
# The f key will be used for non-targets and the j key will be used for targets
# Accuracy and reaction time of each response will be recorded
# A block will consist of 12 trials. Below is the breakdown of the trial types for each version of the task: 
    # 1-back: 3 targets, 9 non-targets 
    # 2-back: 3 targets, 3 lures, 6 non-targets 
    # 3-back: 3 targets, 3 lures, 6 non-targets 
    
# Each letter stimulus will be presented for 0.5 seconds, with a fixed ISI of 1.5 seconds (during which a fixation cross will be on screen) 
# Two output files will be generated - one output file for their practice session and another for the experiment session, which are stored in separate folders
# During the experiment, participants will complete four 1-back blocks, seven 2-back blocks, and seven 3-back blocks 
# The order in which they complete the blocks will be randomzied 
# I have created several CSV files with the letter sequence participants will be shown for each block 
# NOTE: When running this experiment you will need to press 1 to advance from the practice to the test


############## EXPERIMENT CODE STARTS HERE ##############################################

#%% Required set up 

import numpy as np
import pandas as pd
import os, sys, re
import random
from psychopy import visual, core, event, gui, logging

# show the dialog box, create a field for subject ID and session number
subgui = gui.Dlg()
subgui.addField("Subject ID:")
subgui.addField("Session Number:")

# show the gui
subgui.show()

# put the inputted data in easy to use variables
subjID = subgui.data[0]
sessNum = subgui.data[1]

# if the file name already exists, give a notification and exit out of the experiment
ouputFileName = 'sub'+subjID+'_'+'sess'+sessNum+'prac.csv' # prac indicates that the output file is for the practice portion of the task 
if os.path.isfile(ouputFileName) :
    sys.exit("data for this session already exists")

#%% set up study  

# pressing q will quit 
event.globalKeys.add(key='q', func=core.quit)

# open a white full screen window
win = visual.Window(fullscr=True, allowGUI=False, color='white', unit='height') 


###################### BEGIN WITH PRACTICE ############################################################### 

# components for the stimulus display 
myTextF = visual.TextStim(win, text="f = non-target", pos = (-0.25,-0.5), color="black") 
myTextJ = visual.TextStim(win, text="j = target", pos = (0.25,-0.5), color="black") 

# feedback display
corFeedback = visual.TextStim(win, text='correct!', pos=(0,0), color="green")
incFeedback = visual.TextStim(win, text='wrong!', pos=(0,0), color="red")

# fixation display 
fixation = visual.TextStim(win, text="+", color="black")

# output pandas dataframe 
out = pd.DataFrame(columns=['trial','response','rt','correct','letter','block','task_filename'])

# define sum_acc, sum_rt, and num_trials for generating summary statistics 
sum_acc = 0 
sum_rt = 0  
num_trials = 0 

# participant will completing 3 versions of the n-back: 1-back, 2-back and 3-back
n_type = [1,2,3]

#%% task instructions before starting the PRACTICE 

welcome = visual.ImageStim(win, image='instruction_files/welcome.png', pos=(0,0), size=(2,2)) 
welcome.draw()
win.flip()
event.waitKeys(keyList=['1'])

for i in n_type: # created a for loop to present the instructions for 1-back, 2-back and 3-back
    instructions = visual.ImageStim(win, image= 'instruction_files/'+str(i)+'-back.png', pos=(0,0), size=(2,2)) 
    instructions.draw()
    win.flip()
    event.waitKeys(keyList=['1'])

practiceinstruct_1 = visual.ImageStim(win, image='instruction_files/practice_1.png', pos=(0,0), size=(2,2)) 
practiceinstruct_1.draw()
win.flip()
event.waitKeys(keyList=['1'])

practiceinstruct_2 = visual.ImageStim(win, image='instruction_files/practice_2.png', pos=(0,0), size=(2,2)) 
practiceinstruct_2.draw()
win.flip()
event.waitKeys(keyList=['1'])


stimDur = 0.5 # want to present the stimulus for 1 second
fixDur = 1.5 # want to present the fixation for 1.5 seconds (ISI)

# define the clock to record time - need two clocks to get the RT for each trial (rather than an overall experiment time)
expClock = core.Clock()
expClock2 = core.Clock()

#%% This is the PRACTICE SESSION

for i in n_type:
    df = pd.read_csv('prac_csv_files/'+'trial_cond_'+str(i)+'prac.csv')# read in experiment info - indicates what is the correct response for each letter stimulus
    getready = visual.ImageStim(win, image='instruction_files/getready_'+str(i)+'back.jpg', pos=(0,0), size=(2,2)) 
    getready.draw()
    win.flip()
    event.waitKeys(keyList=['1'])
    
    fixation.draw()
    win.flip()
    core.wait(3)
    
    for trial in range(len(df)): 
        event.clearEvents() # only want to register one key press  
        num_trials += 1
        thisStimName = df.letter[trial] # index the items in the stimulus list 
    
        # define the stimuli and text to use for the experiment 
        thisStim = visual.ImageStim(win, image='letters'+'/'+ thisStimName + '.jpg', pos=(0,0), size=(1.5,1.5)) # give path to stimulus (using thisStimName)
    
        # draw the text and the stimulus 
        thisStim.draw() 
        myTextF.draw()
        myTextJ.draw()
        # flip it
        win.flip()
    
        #reset the first experiment clock
        expClock.reset()
    
        #reset the second experiment clock
        expClock2.reset()
    
        #setting the experiment clock here - display the letter and text as long as it is less than the stimulus duration
        while expClock.getTime() < stimDur:  
            thisStim.draw() # draw the text and the stimulus 
            myTextF.draw()
            myTextJ.draw()
            win.flip() # flip it
        
        #reset the first clock
        expClock.reset()
    
        while expClock.getTime() < fixDur: #display the fixation as long as it is less than the fixation duration
            fixation.draw() # draw the fixation 
            win.flip() # flip it

        #reset the clock
        expClock.reset()
    
        # define which keys are valid responses and record the amount of time it takes to make a response 
        keys = event.getKeys(keyList=['f','j'],timeStamped=expClock2) 
        # using event.getKeys instead of event.waitkeys because we do not want to wait for a key response to advance to the next trial
    
    # PROVIDE FEEDBACK
     
    # compare the participant's key response to the correct key response for that stimulus 
    # if they are the same, the response is correct 
    # if they are different, the response is wrong 
    #filtered = trialInfo.loc[trialInfo['letter'] == trial] # take the whole row for that trial 
    #if len(keys) will need an if statement because not requiring a key press
        filtered = df.corr_resp[trial]
        if len(keys) > 0: 
            if keys[0][0] == 'j' and filtered == 'j':  # trialInfo.letter[trial]
                out.loc[trial,'correct'] = 1 # save the accuracy information to the output file, 1 is correct, 0 is incorrect
                corFeedback.draw()
            elif keys[0][0] == 'f' and filtered == 'f': 
                out.loc[trial,'correct'] = 1
                corFeedback.draw()
            else:
                out.loc[trial,'correct'] = 0
                incFeedback.draw() 
        else: #if no key is pressed, want the experiment to continue, and the feedback provided to be incorrect
            keys = np.empty([1,2]) # make keys an empty numpy array (no key is pressed, so there is nothing for keys)
            out.loc[trial,'correct'] = 0
            incFeedback.draw()
        win.flip()
        core.wait(0.5)
    
        sum_acc += out.correct[trial]
    
        #record relevant trial info & save it to a csv file 
        out.loc[trial,'trial'] = trial+1
        out.loc[trial,'response'] = keys[0][0]# [0][0] is referring to columns, if it were [1][0] then it would be referring to rows
        out.loc[trial,'rt'] = keys[0][1]
        out.loc[trial,'letter'] = thisStimName
        out.loc[trial,'block'] = i
        out.loc[[trial]].to_csv('PRACTICE_data/'+ouputFileName,mode='a',header=False,index=False) # have to make header False, or else with all a header for each trial
    
    # GIVE THEM THE OPTION TO REPEAT PRACTICE 
    repeat_practice = visual.ImageStim(win, image='instruction_files/repeatprac_'+str(i)+'back.jpg', pos=(0,0), size=(2,2)) 
    repeat_practice.draw()
    win.flip()
    repeat_keys = event.waitKeys(keyList=['y','n'])
    while repeat_keys[0][0] == 'y': # using a while loop - will keep repeating the task if they press 'y'
        getready = visual.ImageStim(win, image='instruction_files/getready_'+str(i)+'back.jpg', pos=(0,0), size=(2,2)) 
        getready.draw()
        win.flip()
        event.waitKeys(keyList=['1'])
    
        fixation.draw()
        win.flip()
        core.wait(3)
    
        for trial in range(len(df)): 
            event.clearEvents() # only want to register one key press  
            num_trials += 1
            thisStimName = df.letter[trial] # index the items in the stimulus list 
    
            # define the stimuli and text to use for the experiment 
            thisStim = visual.ImageStim(win, image='letters'+'/'+ thisStimName + '.jpg', pos=(0,0), size=(1.5,1.5)) # give path to stimulus (using thisStimName)
    
            # draw the text and the stimulus 
            thisStim.draw() 
            myTextF.draw()
            myTextJ.draw()
            # flip it
            win.flip()
    
            #reset the first experiment clock
            expClock.reset()
    
            #reset the second experiment clock
            expClock2.reset()
    
            #setting the experiment clock here - display the letter and text as long as it is less than the stimulus duration
            while expClock.getTime() < stimDur:  
                thisStim.draw() # draw the text and the stimulus 
                myTextF.draw()
                myTextJ.draw()
                win.flip() # flip it
        
            #reset the first clock
            expClock.reset()
    
            while expClock.getTime() < fixDur: #display the fixation as long as it is less than the fixation duration
                fixation.draw() # draw the fixation 
                win.flip() # flip it

            #reset the clock
            expClock.reset()
    
            # define which keys are valid responses and record the amount of time it takes to make a response 
            keys = event.getKeys(keyList=['f','j'],timeStamped=expClock2) 
            # using event.getKeys instead of event.waitkeys because we do not want to wait for a key response to advance to the next trial
    
        # PROVIDE FEEDBACK
     
        # compare the participant's key response to the correct key response for that stimulus 
        # if they are the same, the response is correct 
        # if they are different, the response is wrong 
        #filtered = trialInfo.loc[trialInfo['letter'] == trial] # take the whole row for that trial 
        #if len(keys) will need an if statement because not requiring a key press
            filtered = df.corr_resp[trial]
            if len(keys) > 0: 
                if keys[0][0] == 'j' and filtered == 'j':  # trialInfo.letter[trial]
                    out.loc[trial,'correct'] = 1 # save the accuracy information to the output file, 1 is correct, 0 is incorrect
                    corFeedback.draw()
                elif keys[0][0] == 'f' and filtered == 'f': 
                    out.loc[trial,'correct'] = 1
                    corFeedback.draw()
                else:
                    out.loc[trial,'correct'] = 0
                    incFeedback.draw() 
            else: #if no key is pressed, want the experiment to continue, and the feedback provided to be incorrect
                keys = np.empty([1,2]) # make keys an empty numpy array (no key is pressed, so there is nothing for keys)
                out.loc[trial,'correct'] = 0
                incFeedback.draw()
            win.flip()
            core.wait(0.5)
    
            sum_acc += out.correct[trial]
    
            #record relevant trial info & save it to a csv file 
            out.loc[trial,'trial'] = trial+1
            out.loc[trial,'response'] = keys[0][0]# [0][0] is referring to columns, if it were [1][0] then it would be referring to rows
            out.loc[trial,'rt'] = keys[0][1]
            out.loc[trial,'letter'] = thisStimName
            out.loc[trial,'block'] = i
            out.loc[[trial]].to_csv('PRACTICE_data/'+ouputFileName, mode='a',header=False,index=False) # have to make header False, or else with all a header for each trial 
        
        repeat_practice = visual.ImageStim(win, image='instruction_files/repeatprac_'+str(i)+'back.jpg', pos=(0,0), size=(2,2)) 
        repeat_practice.draw()
        win.flip()
        repeat_keys = event.waitKeys(keyList=['y','n'])
        if repeat_keys[0][0] == 'n':
            break # will only break the while loop if they press 'n' 
        
core.wait(1)

# congrats on finishing practice 

done_practice = visual.ImageStim(win, image='instruction_files/Done_practice.jpg', pos=(0,0), size=(2,2)) 
done_practice.draw()
win.flip()
event.waitKeys(keyList=['1']) # the experimenter will know to press 1 to close the experiment 

######################### PRACTICE COMPLETE - START TASK #########################################################################################################

# Start the actual task 

startexp_1 = visual.ImageStim(win, image='instruction_files/startexp_1.jpg', pos=(0,0), size=(2,2)) 
startexp_1.draw()
win.flip()
event.waitKeys(keyList=['1']) 

startexp_2 = visual.ImageStim(win, image='instruction_files/startexp_2.jpg', pos=(0,0), size=(2,2)) 
startexp_2.draw()
win.flip()
event.waitKeys(keyList=['1']) 

# participants will complete 4 blocks of the 1-back, 7 blocks of the 2 back, and 7 blocks of the 3-back
block_type = ['1-one','1-two','1-three','1-four','2-one','2-two','2-three','2-four',
'2-five','2-six','2-seven','3-one','3-two','3-three','3-four','3-five','3-six','3-seven'] 

random.shuffle(block_type) # randomize the block order

# want the output file name for the task to be different than the output file name for practice 
ouputFileName_task = 'sub'+subjID+'_'+'sess'+sessNum+'task.csv'

for i in block_type:
    m = (re.split("[-]", i)[-2]) # taking the first element of i --> for example, if i = '2-one', want to take '2'... another example, if i = '3-four', want tot take '3'
    df = pd.read_csv('task_csv_files/'+i+'task.csv')# read in experiment info - indicates what is the correct response for each letter stimulus
    getready = visual.ImageStim(win, image='instruction_files/getready_'+m+'back.jpg', pos=(0,0), size=(2,2)) 
    getready.draw()
    win.flip()
    event.waitKeys(keyList=['1'])
    
    fixation.draw()
    win.flip()
    core.wait(3) # display the fixation cross for 3 seconds before starting the task
    
    for trial in range(len(df)): 
        event.clearEvents() # only want to register one key press  
        num_trials += 1
        thisStimName = df.letter[trial] # index the items in the stimulus list 
    
        # define the stimuli and text to use for the experiment 
        thisStim = visual.ImageStim(win, image='letters'+'/'+ thisStimName + '.jpg', pos=(0,0), size=(1.5,1.5)) # give path to stimulus (using thisStimName)
    
        # draw the text and the stimulus 
        thisStim.draw() 
        myTextF.draw()
        myTextJ.draw()
        # flip it
        win.flip()
    
        #reset the first experiment clock
        expClock.reset()
    
        #reset the second experiment clock
        expClock2.reset()
    
        #setting the experiment clock here - display the letter and text as long as it is less than the stimulus duration
        while expClock.getTime() < stimDur:  
            thisStim.draw() # draw the text and the stimulus 
            myTextF.draw()
            myTextJ.draw()
            win.flip() # flip it
        
        #reset the first clock
        expClock.reset()
    
        while expClock.getTime() < fixDur: #display the fixation as long as it is less than the fixation duration
            fixation.draw() # draw the fixation 
            win.flip() # flip it

        #reset the clock
        expClock.reset()
    
        # define which keys are valid responses and record the amount of time it takes to make a response 
        keys = event.getKeys(keyList=['f','j'],timeStamped=expClock2) 
        # using event.getKeys instead of event.waitkeys because we do not want to wait for a key response to advance to the next trial
    
    # DURING THE EXPERIMENT, NO FEEBACK IS PROVIDED, so only record their key press
        filtered = df.corr_resp[trial]
        if len(keys) > 0: 
            if keys[0][0] == 'j' and filtered == 'j':  # trialInfo.letter[trial]
                out.loc[trial,'correct'] = 1 # save the accuracy information to the output file, 1 is correct, 0 is incorrect
            elif keys[0][0] == 'f' and filtered == 'f': 
                out.loc[trial,'correct'] = 1
            else:
                out.loc[trial,'correct'] = 0
        else: #if no key is pressed, want the experiment to continue, and the feedback provided to be incorrect
            keys = np.empty([1,2]) # make keys an empty numpy array (no key is pressed, so there is nothing for keys)
            out.loc[trial,'correct'] = 0
        
        sum_acc += out.correct[trial]
    
        #record relevant trial info & save it to a csv file 
        out.loc[trial,'trial'] = trial+1
        out.loc[trial,'response'] = keys[0][0]# [0][0] is referring to columns, if it were [1][0] then it would be referring to rows
        out.loc[trial,'rt'] = keys[0][1]
        out.loc[trial,'letter'] = thisStimName
        out.loc[trial,'block'] = m
        out.loc[trial,'task_filename'] = i
        out.loc[[trial]].to_csv('TASK_data/'+ouputFileName_task,mode='a',header=False,index=False) # may want to change the output file name to have a separate practice folder and actual task folder 

# Thank you - you're finished the experiment 
youre_done = visual.ImageStim(win, image='instruction_files/youre_done.jpg', pos=(0,0), size=(2,2)) 
youre_done.draw()
win.flip()
event.waitKeys(keyList=['1']) 







