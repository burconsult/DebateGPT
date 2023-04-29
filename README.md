# DebateGPT
 A GPT powered Streamlit app for debates
 
 ![DebateGPT Logo](https://raw.githubusercontent.com/burconsult/DebateGPT/main/static/logo.svg)

## Introduction

This whole project started as an experiment in creating prompts for ChatGPT to act as tyhe two sides of a university debate.
The blog article about the prompts is here [A prompt for GPT-4 powered debate teams](https://blueberrythoughts.com/2023/04/21/a-prompt-for-gpt-4-powered-debate-teams/).

## Building with Streamlit

After testing the prompts in ChatGPT, I have decided to build a simple script in Python for running the prompts against the OpenAI API. I've then found oput about Streamlit and thought about giving it a try. It was a fun learning and building process so far.

## About the app

The app is quite simple, it lets the user provide a topic for the debate in the form of "This house believes that (topic)." and choose how many rounds the debate will have. There are some final reflections from both "teams" at the end. When the debate is over, it's saved to a SQLite database and to a simple PDF file. Previous debates can be viewed and downloaded as PDF.

## The Cloud App

The cloud app is available here [DebateGPT](https://burconsult-debategpt-debategpt-7ple3d.streamlit.app/) on the Streamlit Community Cloud. It's a quick and fun way to deploy apps built with Streamlit.
