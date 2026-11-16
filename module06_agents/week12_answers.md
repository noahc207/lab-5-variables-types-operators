# Week 12 answers

## Exercise 1
1. The messages the customer typed: 
I want to change my shipping address, its order a102, 9 pine street, tampa.

2. How many tool requests were refused, and why:
Two were denied. The model made up an order ID (A100) and then a made-up address that the customer never gave. The tool only accepts values the customer actually said.

3. If the customer now types "thanks", how many messages does Ollama receive on the next call?
14 messages including the first system message, then the 6 user and assistant messages, 2 for the 3 tool entries, and then the final message

4. Why does "Do you sell gift cards?" still go to a person, and why is that acceptable?
The word "card" is on the handoff word list, so a rule sends it to a person before the model sees it. That's acceptable because a needless handoff costs only a little staff time, while a payment topic handled wrongly put the card details in front of the model.