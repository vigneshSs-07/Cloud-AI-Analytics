### About:
* Google Cloud Pub/Sub is an asynchronous global messaging service. There are three terms in Pub/Sub that appear often: 
    1. Topics
    2. Publishing
    3. Subscribing.

1. A topic is a shared string that allows applications to connect with one another through a common thread.
2. Publishers push (or publish) a message to a Cloud Pub/Sub topic.
3. Subscribers make a "subscription" to a topic where they will either pull messages from the subscription or configure webhooks for push subscriptions. Every subscriber must acknowledge each message within a configurable window of time.
4. To sum it up, a producer publishes messages to a topic and a consumer creates a subscription to a topic to receive messages from it.

### Task 0.
1. Reinitialize Cloud SDK and follow the instructions
gcloud init

### Task 1. Pub/Sub topics
1. Create topic in Pub/Sub
gcloud pubsub topics create myTopic

2. For good measure, create two more topics; one called Test1 and the other called Test2:
a. gcloud pubsub topics create Test1
b. gcloud pubsub topics create Test2

3. To see the three topics you just created, run the following command:
a. gcloud pubsub topics list

4. Time to clean up. Delete Test1 and Test2 by running the following commands:
gcloud pubsub topics delete Test1
gcloud pubsub topics delete Test2

### Task 2. Pub/Sub subscriptions - 
1. Run the following command to create a subscription called mySubscription to topic myTopic:
gcloud  pubsub subscriptions create --topic myTopic mySubscription

2. Add another two subscriptions to myTopic. Run the following commands to make Test1 and Test2 subscriptions:
gcloud  pubsub subscriptions create --topic myTopic Test1
gcloud  pubsub subscriptions create --topic myTopic Test2

3. Run the following command to list the subscriptions to myTopic:
gcloud pubsub topics list-subscriptions myTopic

4. delete the Test1 and Test2 subscriptions. Run the following commands:
gcloud pubsub subscriptions delete Test1
gcloud pubsub subscriptions delete Test2

### Task 3. Pub/Sub publishing and pulling a single message
1. Publish a Message to Topic -- To publish the message "hello" to the topic you created previously (myTopic):
gcloud pubsub topics publish myTopic --message "Hello"
gcloud pubsub topics publish myTopic --message="hello foodies" --attribute="locale=english,username=gcp"

2. Publish a few more messages to myTopic. Run the following commands:
gcloud pubsub topics publish myTopic --message "Publisher's name is Farooqui"
gcloud pubsub topics publish myTopic --message "Publisher likes to eat Non-veg"
gcloud pubsub topics publish myTopic --message "Publisher thinks Pub/Sub is awesome"

3. Check if Subcriber received the earlier message published on Topic
gcloud pubsub subscriptions pull mySubscription --auto-ack 
gcloud pubsub subscriptions pull Test1 --auto-ack

### Task 4. Pub/Sub pulling all messages from subscriptions
1. Run the following commands:
gcloud pubsub topics publish myTopic --message "Publisher is starting to get the hang of Pub/Sub"
gcloud pubsub topics publish myTopic --message "Publisher wonders if all messages will be pulled"
gcloud pubsub topics publish myTopic --message "Publisher will have to test to find out"

# Add a flag to your command so you can output all three messages in one request.
You may have not noticed, but you have actually been using a flag this entire time: the --auto-ack part of the pull command is a flag that has been formatting your messages into the neat boxes that you see your pulled messages in.

### limit is another flag that sets an upper limit on the number of messages to pull.
gcloud pubsub subscriptions pull mySubscription --auto-ack --limit=5