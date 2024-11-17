# LightFeet: Your Nighttime Navigation Guide

### Overview
**LightFeet** is a solution designed to enhance pedestrian safety at night by providing detailed analysis of lighting conditions along walking routes. By leveraging AI-powered lamppost identification and mapping, LightFeet helps users minimize potential safety risks when traveling after dark.

### Problem Statement
Pedestrian safety is a significant concern during nighttime. According to the **Federal Highway Administration**, 76% of pedestrian fatalities occur in dark conditions, even though only 25% of traffic occurs after dark (US DOT, 2024). Simply installing more streetlights isn't always feasible due to the high costs involved\u2014for instance, the estimated cost of pedestrian-scale lighting was $610,000 for just 34 poles in 2015 (Markowitz et al., 2017).

### Our Solution
LightFeet aims to empower pedestrians by analyzing the lighting infrastructure in advance and identifying potential safety risks. Using cutting-edge image processing and artificial intelligence, LightFeet provides users with information about how well-lit a chosen walking route is.

### How It Works
1. **User Inputs Destination**: Users input their desired destination into the app.
2. **Route Identification**: The app identifies possible walking routes.
3. **Street View Images**: Google Street View images along the route are queried.
4. **Lamppost Identification**: AI models analyze these images to identify lampposts.
5. **Light Score Computation**: A "light" score is computed based on the identified lampposts.
6. **Report Dangerous Routes**: Potentially dangerous routes are flagged for users.

### Key Features
- **Google Maps Integration**: Integrated with Google Maps API, allowing access to accurate Street View images along the route.
- **AI-Powered Lamppost Identification**: Uses a blend of image processing techniques and transformer models to identify diverse lampposts.
- **Live User Feedback**: Enables users to provide feedback about lighting conditions to improve the accuracy and reach of LightFeet.

### Technical Details
- **Street View Image Query**: Utilizes the Google Maps API to access images of the user's route.
- **Lamppost Detection**: Combines SAM Segmentation with OpenAI's CLIP (Visual Language Transformer) to accurately identify lampposts from images.
- **Light Score Calculation**: The Light Score is calculated by overlaying lamppost data onto a map and processing it with deep learning models.

### Social Good Opportunity
- **City Infrastructure Improvements**: Partnering with municipalities to identify where new streetlights are most needed based on user feedback.
- **Enhanced Pedestrian Safety**: Minimizing the risk of overestimating safety metrics through deep learning-based data processing.
- **3rd Space Equity**: Providing safe walking alternatives that reduce dependence on expensive options like Uber or personal vehicles, thus promoting equitable access to social spaces.

### Contributors
- Akshat J.
- Daeyoung K.
- Dexter F.
- Dokyun K.
