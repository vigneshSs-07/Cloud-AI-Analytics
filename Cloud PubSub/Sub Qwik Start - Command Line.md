# Google Cloud Pub/Sub: Qwik Start - Command Line

https://partner.cloudskillsboost.google/course_sessions/5692160/labs/408095


Overview
Google Cloud Pub/Sub is a messaging service for exchanging event data among applications and services. By decoupling senders and receivers, it allows for secure and highly available communication between independently written applications. Google Cloud Pub/Sub delivers low-latency/durable messaging, and is commonly used by developers in implementing asynchronous workflows, distributing event notifications, and streaming data from various processes or devices.

What you'll learn
In this lab, you will do the following:

Learn the basics of Pub/Sub.
Create, delete, and list Pub/Sub topics.
Create, delete, and list Pub/Sub subscriptions.
Publish messages to a topic.
Use a pull subscriber to output individual topic messages.
Use a pull subscriber with a flag to output multiple messages.


### Pub/Sub basics
As stated earlier, Google Cloud Pub/Sub is an asynchronous global messaging service. There are three terms in Pub/Sub that appear often: topics, publishing, and subscribing.

A topic is a shared string that allows applications to connect with one another through a common thread.

Publishers push (or publish) a message to a Cloud Pub/Sub topic.

Subscribers make a "subscription" to a topic where they will either pull messages from the subscription or configure webhooks for push subscriptions. Every subscriber must acknowledge each message within a configurable window of time.

To sum it up, a producer publishes messages to a topic and a consumer creates a subscription to a topic to receive messages from it.

### Task 1. Pub/Sub topics
Pub/Sub comes preinstalled in the Google Cloud Shell, so there are no installations or configurations required to get started with this service.

Run the following command to create a topic called myTopic:
gcloud pubsub topics create myTopic
Copied!
Test completed task

Click Check my progress to verify your performed task. If you have completed the task successfully you will be granted an assessment score.

Create a Pub/Sub topic.
For good measure, create two more topics; one called Test1 and the other called Test2:
gcloud pubsub topics create Test1
Copied!
gcloud pubsub topics create Test2
Copied!
To see the three topics you just created, run the following command:
gcloud pubsub topics list
Copied!
Your output should resemble the following:

name: projects/qwiklabs-gcp-3450558d2b043890/topics/myTopic
---
name: projects/qwiklabs-gcp-3450558d2b043890/topics/Test2
---
name: projects/qwiklabs-gcp-3450558d2b043890/topics/Test1
Time to clean up. Delete Test1 and Test2 by running the following commands:
gcloud pubsub topics delete Test1
Copied!
gcloud pubsub topics delete Test2
Copied!
Run the gcloud pubsub topics list command one more time to verify the topics were deleted:
gcloud pubsub topics list
Copied!
You should get the following output:


### ask 2. Pub/Sub subscriptions
Now that you're comfortable creating, viewing, and deleting topics, time to work with subscriptions.

Run the following command to create a subscription called mySubscription to topic myTopic:
gcloud  pubsub subscriptions create --topic myTopic mySubscription
Copied!
Test completed task

Click Check my progress to verify your performed task. If you have completed the task successfully you will be granted an assessment score.

Create Pub/Sub Subscription.
Add another two subscriptions to myTopic. Run the following commands to make Test1 and Test2 subscriptions:
gcloud  pubsub subscriptions create --topic myTopic Test1
Copied!
gcloud  pubsub subscriptions create --topic myTopic Test2
Copied!
Run the following command to list the subscriptions to myTopic:
gcloud pubsub topics list-subscriptions myTopic
Copied!
Your output should resemble the following:

---
  projects/qwiklabs-gcp-3450558d2b043890/subscriptions/Test2
---
  projects/qwiklabs-gcp-3450558d2b043890/subscriptions/Test1
---
  projects/qwiklabs-gcp-3450558d2b043890/subscriptions/mySubscription
Test your understanding

Below are multiple choice questions to reinforce your understanding of this lab's concepts. Answer them to the best of your abilities.


To receive messages published to a topic, you must create a subscription to that topic.

True

False

Now delete the Test1 and Test2 subscriptions. Run the following commands:
gcloud pubsub subscriptions delete Test1
Copied!
gcloud pubsub subscriptions delete Test2
Copied!
See if the Test1 and Test2 subscriptions were deleted. Run the list-subscriptions command one more time:
gcloud pubsub topics list-subscriptions myTopic
Copied!
You should get the following output:


### Task 3. Pub/Sub publishing and pulling a single message
Next you'll learn how to publish a message to a Pub/Sub topic.

Run the following command to publish the message "hello" to the topic you created previously (myTopic):
gcloud pubsub topics publish myTopic --message "Hello"
Copied!
Publish a few more messages to myTopic. Run the following commands (replacing <YOUR NAME> with your name and <FOOD> with a food you like to eat):
gcloud pubsub topics publish myTopic --message "Publisher's name is <YOUR NAME>"
Copied!
gcloud pubsub topics publish myTopic --message "Publisher likes to eat <FOOD>"
Copied!
gcloud pubsub topics publish myTopic --message "Publisher thinks Pub/Sub is awesome"
Copied!
Next, use the pull command to get the messages from your topic. The pull command is subscription based, meaning it should work because earlier you set up the subscription mySubscription to the topic myTopic.

Use the following command to pull the messages you just published from the Pub/Sub topic:
gcloud pubsub subscriptions pull mySubscription --auto-ack
Copied!
Your output should resemble the following:

Three-column table with the headings: Data, Message_ID, and Attributes.The Data column contains the following: Publisher likes to eat <FOOD>.

What's going on here? You published 4 messages to your topic, but only 1 was outputted.

Now is an important time to note a couple features of the pull command that often trip developers up:

Using the pull command without any flags will output only one message, even if you are subscribed to a topic that has more held in it.
Once an individual message has been outputted from a particular subscription-based pull command, you cannot access that message again with the pull command.
To see what the second bullet is talking about, run the last command three more times. You will see that it will output the other messages you published before.

Now, run the command a 4th time. You'll get the following output (since there were none left to return):

gcpstaging20394_student@cloudshell:~ (qwiklabs-gcp-3450558d2b043890)$ gcloud pubsub subscriptions pull mySubscription --auto-ack
Listed 0 items.
In the last section, you will learn how to pull multiple messages from a topic with a flag.


### Task 4. Pub/Sub pulling all messages from subscriptions
Since you pulled all of the messages from your topic in the last example, populate myTopic with a few more messages.

Run the following commands:
gcloud pubsub topics publish myTopic --message "Publisher is starting to get the hang of Pub/Sub"
Copied!
gcloud pubsub topics publish myTopic --message "Publisher wonders if all messages will be pulled"
Copied!
gcloud pubsub topics publish myTopic --message "Publisher will have to test to find out"
Copied!
Add a flag to your command so you can output all three messages in one request.
You may have not noticed, but you have actually been using a flag this entire time: the --auto-ack part of the pull command is a flag that has been formatting your messages into the neat boxes that you see your pulled messages in.

limit is another flag that sets an upper limit on the number of messages to pull.

Wait a minute to let the topics get created. Run the pull command with the limit flag:
gcloud pubsub subscriptions pull mySubscription --auto-ack --limit=3
Copied!
Your output should match the following:

Three-column table with the headings: Data, Message_ID, and Attributes. The Data column contains three lines of data.

Now you know how to add flags to a Pub/Sub command to output a larger pool of messages. You are well on your way to becoming a Pub/Sub master.

