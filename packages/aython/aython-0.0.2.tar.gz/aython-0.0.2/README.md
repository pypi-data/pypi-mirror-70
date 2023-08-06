# Aython Package
##### A small easy to use interface for python based alexa skills

#####Installing
>pip install aython  
>https://ngrok.com/download

##### How to use
>see example.py for use

##### Usage / Setting up on amazon
   >sign up for an amazon developer account  
>navigate to alexa -> create alexa skills -> console  
>create a new skill   
>select custom model and "provision your own" backend and start from scratch  
>create an invocation name
>create a new intent called hello  
>give hello as the sample utterance  
>amazon requires and ssl certificate so ngrok is needed  
>open nrgok py running "ngrok.exe http 5000" in the same folder  
>copy the https forwarding address and paste into default region
>select ssl certificate as a sub-domain
>click build  
>run the example.py script
>test the skill by open the skill with the invocation name  
>type hello to run the hello intent   

##### More options
    launch_message   
    intent_function    
    session_start_function  
    session_end_function   
    help_function  
>These options can all be change with the command aython.alexa."thing_to_change" 
