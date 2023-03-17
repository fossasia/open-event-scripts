# open-event-scripts

Useful scripts for managing events using Open Event API

## Syestem Requirements
Before installing open-event-scripts, make sure that your system meets the following requirements:

    - python 3.x 
    - pip package manager 
    
## Installation Steps
Follow these steps to install the open-event-scripts.

1. Clone the open-event-scripts repository: 

    ``` git clone https://github.com/fossasia/open-event-scripts.git ```
 
2. Change into open-event-scripts:
 
   ```  cd open-event-scripts ```
 
 3. Install the required python packages using pip: 

     ``` pip install -r requirements.txt ```

    Or using: 

     ``` peotry install ```
     

     ```peotry shell ```

        
## Usage
Use this script to change the event schedule: 

  ```
  python scripts/reschedule.py <event_identifier>
  ```

Use this script to generate session of tweets: 

  ```
  python scripts/generate_session_tweet_csv.py <event_identifier>
  ```
