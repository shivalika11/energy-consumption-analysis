# Energy Consumption Analysis & Optimization System

A cloud-based web application that helps small businesses understand their electricity consumption, identify unusual usage patterns, and discover potential energy-saving opportunities.

The system allows users to upload electricity bills and historical consumption data, analyze usage patterns, and view insights and rule-based recommendations through a dashboard.

The project combines Python-based data analysis with AWS cloud services to demonstrate a practical cloud application.

---

## Overview

Electricity costs are an important operating expense for small businesses. However, many businesses do not regularly analyze their electricity consumption or identify periods when usage is unusually high.

The Energy Consumption Analysis & Optimization System aims to address this problem by providing a simple platform for analyzing electricity consumption data.

Users can upload electricity bills and consumption datasets. The system processes the uploaded information, calculates consumption statistics, identifies potential inefficiencies, and presents the results through a visual dashboard.

The application is intended for small offices, retail stores, workshops, and other small businesses that want a clearer understanding of their electricity usage.

## Problem Statement

Small businesses may receive electricity bills and meter readings without having an easy way to understand their consumption patterns.

Manually reviewing electricity data can make it difficult to identify:

- Periods of unusually high electricity consumption.
- Consumption occurring outside normal working hours.
- Differences between working-day and weekend consumption.
- High consumption during low-occupancy periods.
- Potential opportunities to reduce unnecessary electricity usage.

This project aims to simplify the process by combining file uploads, automated data processing, cloud storage, and visual reporting.

## Objectives

- Develop a web application for uploading electricity bills and consumption datasets.
- Store uploaded files securely using Amazon S3.
- Extract relevant information from supported electricity bills using Amazon Textract.
- Process CSV and Excel consumption data using Python, Pandas, and NumPy.
- Calculate daily averages, peak consumption, and other useful statistics.
- Identify potential after-hours and low-occupancy consumption patterns.
- Generate basic rule-based energy-saving recommendations.
- Present results through an interactive dashboard.
- Deploy the application on AWS infrastructure.
- Apply containerization, automated testing, and CI/CD practices.

## Key Features

### 1. User Registration and Login

Users can create an account and access the application.

The backend will validate registration details and handle passwords securely. Authentication and user data storage will be implemented using appropriate server-side security practices.

### 2. Business Profile Management

Users can provide basic information about their business, including:

- Business name.
- Business type.
- Opening and closing hours.
- Lunch or low-occupancy periods.
- Main electrical equipment.

This information helps the analysis component interpret consumption patterns in the context of normal business operations.

### 3. Electricity Bill Upload

Users can upload supported electricity bills in PDF or image formats.

Uploaded files will be stored in Amazon S3. Amazon Textract will be used to extract available billing information, such as:

- Billing period.
- Electricity units consumed.
- Bill amount.
- Meter readings, when available.

Extracted information will be validated before being used in the application.

Extraction accuracy may vary depending on the bill format, image quality, and available information.

### 4. Consumption Dataset Upload

Users can upload historical electricity consumption data in CSV or Excel format.

The application will process the data using Pandas and NumPy.

Supported datasets will follow a documented structure containing appropriate time and consumption fields.

Sample datasets will be provided so that the project can be demonstrated without depending on access to real business electricity records.

### 5. Electricity Consumption Analysis

The analysis component will calculate useful consumption statistics, including:

- Total electricity consumption.
- Average daily consumption.
- Peak recorded consumption.
- Consumption trends over time.
- Consumption during working and non-working hours, where the dataset supports the calculation.
- Weekend versus weekday consumption, where applicable.
- Potentially unusual or elevated consumption patterns.

The analysis will depend on the quality and structure of the uploaded dataset.

### 6. Energy-Saving Recommendations

The application will generate simple, rule-based recommendations from the available consumption data and business profile.

Examples include:

- Reviewing electricity consumption outside normal working hours.
- Investigating elevated usage during low-occupancy periods.
- Comparing weekend consumption with normal working-day consumption.
- Reviewing operating schedules for non-essential equipment.

Recommendations will identify potential areas for investigation rather than claim to prove that a particular appliance is wasting electricity.

### 7. Interactive Dashboard

The dashboard will present the results of the analysis using charts, summary statistics, and recommendations.

The interface will use Chart.js to display supported metrics and consumption trends.

Dashboard values will ultimately be generated from processed user data rather than fixed demonstration values.

### 8. Cloud Storage and Processing

Amazon S3 will provide storage for uploaded electricity bills and consumption datasets.

Amazon Textract will support electricity bill information extraction.

Amazon DynamoDB will store appropriate application data, such as user profiles and analysis metadata.

AWS Lambda and Amazon SNS may be used for focused background processing and notifications where appropriate to the final implementation.

### 9. Monitoring and Deployment

The application is intended to run on Amazon EC2.

Docker will package the application and its dependencies. GitHub Actions will be used for automated testing and deployment workflows.

Amazon CloudWatch will support application monitoring and logging, while AWS IAM will control permissions for accessing AWS resources.

---

## Technology Stack

### Frontend

- HTML5
- CSS3
- Bootstrap
- JavaScript
- Chart.js

### Backend

- Python
- Flask

Flask will handle server-side requests, application routes, authentication workflows, file uploads, AWS integration, and communication between the frontend and analysis components.

### Data Processing

- Pandas
- NumPy

### AWS Cloud Services

| Service | Purpose |
|---|---|
| Amazon EC2 | Hosting the web application |
| Amazon S3 | Storing uploaded electricity bills and consumption datasets |
| Amazon Textract | Extracting information from supported electricity bills |
| Amazon DynamoDB | Storing user profiles and application metadata |
| AWS Lambda | Handling selected background processing tasks |
| Amazon SNS | Sending relevant notifications |
| Amazon CloudWatch | Application logging and monitoring |
| AWS IAM | Managing permissions and access to AWS resources |

AWS services will be integrated as the application is developed. Not every service is required for the application to function, and optional services will only be included where they provide a clear purpose.

### Development and DevOps

- Git
- GitHub
- Docker
- GitHub Actions
- Automated testing
- CI/CD

---

## System Architecture

The application will use a Flask-based web architecture integrated with AWS services.

```text
                    USER
                      |
                      v
              Web Application
             HTML, CSS, JavaScript
                      |
                      v
                  Flask
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
      Amazon S3   DynamoDB    Amazon Textract
          |           |           |
          |           |           v
          |           |     Extracted Bill Data
          |           |           |
          +-----------+-----------+
                      |
                      v
              Python Processing
              Pandas and NumPy
                      |
                      v
             Consumption Analysis
                      |
                      v
           Rule-Based Recommendations
                      |
                      v
               Flask Dashboard
                      |
                      v
                 Chart.js
