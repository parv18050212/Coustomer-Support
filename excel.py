import random
import pandas as pd

# Example categories, sentiments, and escalations
categories = ['Account', 'Billing', 'Technical', 'Refund', 'Feedback', 'Upgrade', 'Service']
sentiments = ['Positive', 'Neutral', 'Negative']
escalations = [0, 1]  # 0 = No Escalation, 1 = Escalate

# Sample queries for different customer support scenarios
queries = [
    'How do I reset my password?', 'What are the billing details for last month?',
    'My internet is not working, please help.', 'I would like a refund for the overcharge.',
    'Your service is great, thanks for the help!', 'I want to upgrade my plan to the premium one.',
    'The website is not loading, can you help?', 'I need a technician to install the new software.',
    'How can I check my account balance?', 'My account is locked, I cannot access it.',
    'Why did I get charged twice this month?', 'Can you help me track my package?',
    'I am not happy with the quality of the service.', 'How do I cancel my subscription?',
    'Can I speak to a supervisor regarding my issue?', 'I would like to change my email address.',
    'I received a damaged product, can I get a refund?', 'Why is my internet so slow today?',
    'How can I upgrade to a faster internet plan?', 'I was charged incorrectly, can you explain?',
    'Your service is very reliable, I’m happy with it.', 'How can I access my invoice for last month?',
    'I want to report a fraudulent activity on my account.', 'Your customer service is very unhelpful.',
    'Can I update my shipping address?', 'I’m having trouble with the Wi-Fi connection.',
    'How can I view my recent transactions?', 'I want to add a new feature to my account.',
    'Can you help me with my subscription renewal?', 'The technician missed the scheduled appointment.',
    'Why is my account locked again?', 'I want to speak with someone in customer support.',
    'I want a refund for the payment I made last month.', 'How can I disable my account temporarily?',
    'I’m experiencing issues with the website login.', 'I’d like to change my payment method.',
    'The support team has not been helpful at all.', 'Can I update my payment details?',
    'I received an incorrect bill, can I get clarification?', 'How do I change my subscription plan?',
    'The refund process has been taking too long.', 'I have a complaint about the recent product.',
    'Can I get a refund for the extra charges on my bill?', 'I’m not happy with the service quality.',
    'What is the status of my order?', 'How do I get support for a technical issue?',
    'Can I get a discount on my subscription?', 'I would like to file a complaint about a technician.',
    'I’m interested in adding more services to my plan.', 'I was charged for services I didn’t use.',
    'Why are my internet speeds so low?', 'I want to cancel my subscription due to poor service.',
    'I need assistance with changing my registered email.', 'Can I get a technician to fix my Wi-Fi?',
    'How can I track my order shipment?', 'Can I upgrade my plan to include more data?',
    'I want a refund because the product is faulty.', 'I’d like to file a complaint about a technician.',
    'How do I report an issue with my account?', 'Can I add a secondary email to my account?',
    'How do I change the billing cycle?', 'I want a refund for the subscription charges.',
    'Can I upgrade my plan to get more features?', 'I would like to know the billing details for last month.',
    'The support team has been very helpful, thank you!', 'How do I cancel my service?',
    'Can you explain the charges on my bill?', 'I need help with my billing issue.',
    'I want to escalate my complaint to a supervisor.', 'How do I reset my security question?',
    'How do I unsubscribe from your newsletter?', 'Can you help me check the status of my refund?',
    'Can you help me recover my account password?', 'The customer service is very slow.',
    'I would like to get a discount on my next payment.', 'How do I update my billing address?',
    'The technician was late for the appointment.', 'I can’t find my payment receipt anywhere.',
    'I want to change my payment method, how can I do that?', 'I want to downgrade my subscription plan.',
    'I’m facing issues with account verification.', 'I have not received my refund yet.',
    'How can I report a bug in your software?', 'Can I get a refund for the extra charges on my bill?',
    'I want to upgrade my account to premium services.', 'The connection drops frequently, can you fix it?',
    'How do I cancel my account permanently?', 'I need assistance with subscription cancellation.',
    'I’ve been overcharged, can you help?', 'My internet is not working at all, please help.',
    'How can I get my refund processed faster?', 'Can I change my subscription to another plan?',
    'I need help with resetting my password.', 'Why was I charged for the wrong service?',
    'Can I update my service preferences?', 'I would like to switch to a different plan.',
    'I need a refund for the extra payment charged.', 'Can I report a service outage in my area?',
    'How do I check the status of my service request?', 'Can I change the plan for my subscription?',
    'I’m having trouble accessing my account.', 'How do I reset my security settings?',
    'I’d like to file a complaint about the poor service.', 'How can I check if my payment was processed?',
    'Why is my internet service so slow?', 'Can I change my account details?',
    'I need help with the billing issue.', 'How do I report a fraudulent charge?',
    'I need a technician for an installation service.', 'How do I upgrade my service?',
    'I’m not happy with the service quality, can I cancel?', 'Can I file a complaint about a technician?',
    'How do I contact a customer service representative?', 'Can I report an issue with my billing?',
    'How do I get support for my internet issue?', 'Can I get help with a refund for a faulty product?',
    'I would like to cancel my account due to service issues.', 'How do I escalate my complaint?',
    'I need assistance with my billing questions.', 'I want to upgrade my internet plan.'
]

# Ensure that we have 200 queries
queries = queries[:200]

# Generate a balanced dataset with 200 entries
data = {
    'query': queries,  # 200 queries
    'category': random.choices(categories, k=200),
    'sentiment': random.choices(sentiments, k=200),
    'escalation': random.choices(escalations, k=200)
}

# Check the length of each list to ensure they match
length = len(queries)
print(f"Length of queries: {length}")
print(f"Length of categories: {len(data['category'])}")
print(f"Length of sentiments: {len(data['sentiment'])}")
print(f"Length of escalations: {len(data['escalation'])}")

# If the lengths are not the same, adjust them
if len(data['category']) != length:
    data['category'] = random.choices(categories, k=length)
if len(data['sentiment']) != length:
    data['sentiment'] = random.choices(sentiments, k=length)
if len(data['escalation']) != length:
    data['escalation'] = random.choices(escalations, k=length)

# Create a DataFrame from the data
df = pd.DataFrame(data) 

# Display the first few rows of the dataset
print(df.head())

# Save the dataset to a CSV file
df.to_csv("balanced_customer_support_data.csv", index=False)
