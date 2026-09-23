# IntelliBargainBot

## AI-Driven Price Negotiation System for E-Commerce Platforms

IntelliBargainBot is an AI-powered bargaining chatbot for e-commerce platforms that enables personalized, multi-round price negotiation. The system uses customer purchasing behavior, NLP-based intent detection, and a policy-driven negotiation engine to generate adaptive counter-offers.

## Key Features

- Customer segmentation using K-Means clustering
- Segmentation of customers into New, Regular, and Loyal categories
- RFM-based behavioral feature engineering
- Hybrid NLP-based negotiation intent detection
- Keyword-based intent matching with FalconsAI transformer-based intent detection as a fallback
- Customer offer/price extraction using regular expressions
- Policy-driven negotiation based on customer segment, product demand, and purchase quantity
- Multi-round bargaining using a Polynomial Concession Model
- Interactive chatbot interface

## System Workflow

```text
Customer Adds Product to cart
   ↓
Negotiation through chatbot interface
   ↓
Intent Detection + Offer Extraction
   ↓
Customer Segmentation using K-Means
   ↓
Negotiation Policy based on Customer Segment,
Product Demand, and Purchase Quantity
   ↓
Polynomial Concession Model
   ↓
Counter-Offer
   ↓
Next Negotiation Round
```

## Customer Segmentation

Customer purchasing behavior is analyzed using RFM-derived and behavioral features such as:

Recency
Order frequency
Total spending
Average spending per order
Customer lifetime
Purchase frequency

K-Means clustering is used to classify customers into three segments:

New
Regular
Loyal

The clustering process was evaluated using the Elbow Method, Silhouette Score.

## NLP and Negotiation

The chatbot uses a hybrid NLP approach. Keyword matching handles predefined negotiation intents, while the FalconsAI transformer-based model is used as a fallback for intent detection. Regular expressions are used to extract the price offered by the customer.

The negotiation engine considers the customer's segment, product demand, purchase quantity, and negotiation round to generate adaptive counter-offers. A Polynomial Concession Model controls how the counter-offer changes across multiple negotiation rounds.

## Technology Stack

- **Programming:** Python, JavaScript
- **Backend:** Flask
- **Machine Learning:** Scikit-learn, K-Means
- **Data Processing:** Pandas
- **NLP:** Transformers, FalconsAI
- **Frontend:** React.js
- **Other:** Regular Expressions
  
## How to Run

```bash
cd backend
python app.py

cd frontend
npm install
npm run dev
