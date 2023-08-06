# Capture Grid Bot

Simple application to automate common use  cases with [CaptureGrid4](https://www.kuvacode.com/)

## Installation

The actual application can be installed or upgraded with the following command:

    sudo pip3 install -U capturegridbot --system

## CaptureGrid4 Setup

The easiest way to CaptureGrid4 should be installed via snap. However, due to the strict limitations of the snap 
sandboxing, it is expected that you have installed it with `--devmode`. Otherwise downloading of files might not
work correctly.

Given this, it is best to reinstall the application to make sure that the

    sudo snap remove capturegrid4; sudo snap install capturegrid4 --devmode



