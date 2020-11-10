# A lightweight application framework in Python

## Introduction 

This package is an illustration of how one might implement an application framework in Python. The application doesn't really do anything, but the code illustrates some concepts which is useful to build larger applications.

1. Units of work are encapsulated as __active objects__ which communicate with other objects via a messaging system. 

1. Use of event subject to broadcast user interaction and internal events to listeners. 

1. The use of dependency injection. In this case, we manually wire up the dependencies in the main function. 

1. A lightweight event loop. 

## Running
Clone this repository and install all required dependencies. Then run 
`python -m rtf`. 
