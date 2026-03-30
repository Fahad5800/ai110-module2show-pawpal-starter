# PawPal+ Project Reflection

## 1. System Design
- Allow user to input basic pet infromation and their availability. Pet specificities can include(type, age, and any special need).
- Allow users to edit, add, or remove pet tasks.
- Generate a daily customizable pet plan that can be changed based on time availability, priorities, and owner preferences. 
- To develop the system, I think we need pet, owner, task, and manager (does scheduling) class
**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

---
Response: 
- I chose 4 classes for this project - Pet, Tasks, Schedular, and Owner. Pet and Owner classes represents original owner and an animal in real life. While Task represent the entity of task itself. Schedular is like a manager who allows owner/user to change or edit the schedule. 
- Pet class have name, species, age, and any special needs. Task stores timing, frequency, and priority of the owner. Owner hold's its properties such as name, availability, and preferences to build a plan. Schedular connects all the other classes, pet, tasks, and owner, and is responsible for producing a schedule.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---
Response:
- Owner has no Pet or Task collection: The owner class is not connected with pet and tasks. This makes owner unaware of his pet or tasks in the app.
- Schedular only supports a single pet, in real system, we will be having multiple pets
- Task does not contain any id attribute


## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Response:
- Available hours: If a task needs 30 minutes but only 15 minutes remain, it fails to schedule
- Frequency: The frequency determines when tasks get repeated. Each task must be repeated daily, 
monthly, or yearly. 
- Duration: Tasks has a duration in minutes, the schedular needs to find a contigious free slot that fits it. 
- Priority was chosen because missing high urgency task can be harmful for owner or owner's pet. Duration is secondary; longer tasks are placed first within the same priority level to avoid conflicts of time slots.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Response:
- The schedular uses a greedy approach: it sorts tasks by priorities first, then by duration, then by name, and assigns tasks to the earliest time available that fits. Although, this is not wrong but it can lead to suboptimal schedules where a long task can block the time for multiple shorter tasks later in the day. 
- This tradeoff makes sense to me because looking at the simplicity of the predicatable algorithm is easy to understand and implement. For a pet app with short tasks, and limited owner availability, the greedy method is most reasonable option. 

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

Response:
- AI is used for my UML diagram creation, code and logic implementation, debugging, test cases, and writing Readme.
- The detail, contextual, and tagged '#' prompts were really helpful in getting the answer. One thing that I experienced with AI was, as the complexity of the design increased, the time it took for the AI output also increased. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---
Response:
- I accepted most of them, but some of that did not passed the test cases were immidietly discarded. One scenario was during the implementation of UML diagram. I found that AI code generated did not connected the schedular with other classes. I quickly used AI again for sanity checking and it was verified by test cases that schedualr (manager) class was not fully connected with other classes.
- I evaluated AI suggestion based on reading the code logic and test cases.

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Response:
- I tested task completion status, pet's tasks count, filtering tasks by pet name, sorting tasks based on scheduled time after plan generation, auto resetting and rescehduling after task completion, and multi-day plan generation for a repeating daily task.
- These tasks are important because they cover a full life cycle of a task including creation, scheduling, conflict detection, completion, and recurrence. 


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---
Response:
- I am very confident in my schedular class as it has passes all test cases. Other then known tradeoffs and constraints, I am very confident on this project.
- If more time, I would have tested weekly tasks on a wrong day, februray edge case, especailly for leap year, and tasks longer then 60 minutes test, which should fail becaue eac hhour is an isolated block not a continious period. 

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

Response:
- I am mostly satisfied with internal core logic in main.py. This is because I think main.py serves as a strong foundation for this project that makes the whole project scalable and flexible for future uses.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

Respnse:
- I would have improved the UI. A more colorful one can serve as an attractive platform. In the internal logic, I would have improved that my main.py version more better and would have given more options in schedular class.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Response:
- I learned many things, not just one. I learned how to work with AI, identify AI hellucination, test case strategy (this was totally new thing for me), Development process (from UML to working logic), streamlit, and documentation in github.