# FilamentRecycler

## Table of Contents
1. Introduction
2. Features
3. Design Process
4. Component List
5. Build Instructions

## Introduction

## Features

### OLED Display for Monitoring and Setting Adjustment

### Dual Potentiometers for Control

### PID Temperature Control

### Integrated Cutter with Adjustable Cutting Width

### Motor Driven Spool Holder 

### Filament Feeder Guide Synced with Spool Rotation

## Design Process

### A Quick Note
As a warning, this section was written near the end of the design process after I had completed all prototyping and the majority of the current code. As such I don't know exactly what I was thinking at every point in this process and I do not have a perfect understanding of how I settled on each design decision. I have done my best to make this section representative of my thinking process and how it applied to this project from memory. Now, onto the real content.

### Cutting Assembly
The cutting assembly is responsible for holding any suitable bottle while allowing said bottle to spin freely and be fed through a cutting blade. From the start, I knew I wanted the cutting width to be adjustable to allow tuning for different feed rates, plastic thickness, and plastic types. Initially I planned on using a heavily geared down DC motor for adjustment, but this was changed in favour of a manual system which requires fewer parts and decreases build cost and complexity...

### The Melt Zone
Fun name for the repurposed 3D printer heater block + thermistor that melts and forms the cut bottles into filament. The initial requirement I created for this system is that it would utilize a standard NTK~~ thermistor (*that most 3D printers use*) to allow the microcontroller of choice to safely monitor and control the heater blocks temperature. This provides increased control precision and the possibility of more features than a purely analog heater control.

### Filament Feeder Guide
This is the guide that should allow consistent and tight winding of produced filament around the spool. I was first privvy to the idea of using a similar mechanism to that used by baitcasting/saltwater fishing reels, however 3D printing a cross-cut gear? in a reasonably small diameter proved unfeasible. Rather than using some OTS parts which might be difficult to find, I settled on an oscillating gear mechanism which requires only a few simple printed parts and common pieces of hardware.

### Filament Spool
I knew this would likely be the most mechanically complex piece of the filament recyclers entire design, and as such I went through many design iterations to satisfy my requirements of this part. It needed to be robust, adaptable to support custom printed spools or empty mass produced ones, and contain a drive assembly powerful enough to pull plastic through the melt zone. To achieve the torque and control I wanted (*and also use parts that many 3D printing aficionados might already have laying around*) I decided on a bog standard NEMA 17 stepper motor and A4988 stepper driver. The simple **A4988** can be easily controlled by most (*if not all*) common microcontrollers using one GPIO pin for controlling direction (**HIGH** *or* **LOW**) and another pin for a PWM signal to control when steps occur.

## Component List

### OTS Parts
1. NEMA 17 Stepper Motor
2. A4988 Stepper Motor Driver
3. Raspberry Pi Pico
4. 

### Printed Parts
1. 

### PCB


### Component Substitutions
- I used a rather standard Xmm deep NEMA 17 because it is what I had available. A deeper motor would have more torque and be fine here, and I imagine that a shorter one (even a pancake stepper), would have sufficient torque with the amount of gear reduction used. I recommend a standard length stepper for peace of mind. As for non-stepper motor alternatives, there are numerous small DC motors with integrated gear reduction that would work well (*built in reduction is critical here, as most small DC motors will have a no load RPM in the 10's of thousands, whereas NEMA 17 operate at a few thousand RPM at most*). I will provide a few examples in the appendix [section]. In the event that you choose to use a standard DC motor, a stepper motor driver will not suffice for powering it. I will also provide some options for DC motor control in the appendix [section].

- 

## Build Instructions


