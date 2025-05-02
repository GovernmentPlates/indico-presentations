---
marp: true
title: Rewriting the check-in app
theme: indico
paginate: true
_paginate: false
footer: ''
---
<!-- _footer: '' -->
![bg](assets/slides/splash.png)

![](assets/theme/cern_bw.svg)

<style scoped>
    img {
        margin-left: 15px;
        margin-top: 15px;
        position: absolute;
        top: 0;
        left: 0;
        width: 60px;
        height: 60px;
        }
</style>

---

![width:400px right:50% left:50%](assets/theme/logo.svg)
*Rewriting the Indico check-in app*

### Dominic Hollis - Indico Team (CERN)

<style scoped>
    section {
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }

    h3 {
        color: #aaa;
        font-size: 0.8em;
        font-weight: normal;
    }
</style>
---
![bg left](assets/slides/seats.jpg)

### What is the check-in app?

 - For organizers to check-in attendees at events
 - Used at CERN for (major) events and beyond
 - Does what it says on the tin

---
![bg right](assets/slides/old-engine.jpg)

### Legacy check-in app

 - Built in 2013 (and continued to be developed till 2015)
 - AngularJS
 - Cordova to build for iOS and Android
 - Showing its age
 - Hard to maintain

---

### The legacy check-in app
🪦 2013 - 2023

![height:460px](assets/slides/checkin-legacy-app.png)

<small>GPlay listing removed as of early 2024, App Store listing removed in early April 2025</small>

<style scoped>
    section {
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        padding-bottom: 0 !important;
        padding-top: 0 !important;
    }

    h3 {
        font-size: 1.5em;
        margin-bottom: 0;
    }

    small {
        margin: 0;
        font-size: 0.8em;
        color: #aaa;
    }
</style>

---
![bg left](assets/slides/gears.jpg)
### What is a Progressive Web App (PWA)?
- PWAs are web applications that behave like native apps
- They can work offline and can be installed on devices
- Built using standard web technologies (HTML, CSS, JS)
- Provide a seamless, app-like experience across platforms

---
![bg right](assets/slides/planning.jpg)

### The rewrite

- Idea floated in 2023
- Summer student project (João Mesquita & Tomáš Roun)
- Early ideas involved using React Native, but...
- PWA was chosen instead (more on that later)

---
<style scoped>
    section {
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        padding-bottom: 0 !important;
        padding-top: 0 !important;
    }

    h3 {
        font-size: 1.75em;
        background: linear-gradient(to right,rgb(0, 255, 255),rgb(9, 19, 216));
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>

### The new check-in app
https://checkin.getindico.io

![height:500px](assets/slides/checkin_app.png)

---
![bg right](assets/slides/stack.jpg)
### App Stack
- React (Typescript/TSX)
- Vite (Build)
- Tailwind CSS
- Openshift (Deployment)

---
![bg left](assets/slides/thumbs-up.jpg)
### PWA > React Native

- Single, uniform codebase for both iOS and Android
- Lightweight, easy to develop and maintain
- No need to publish to GPlay/App Store (although, we could in theory)
- Modern PWAs are pretty great these days 👍 (mobile browsers are packing more functionality with each release)

---
![bg right](assets/slides/lighthouse.jpg)

### Lighthouse reporting (Chrome)

- Performance, accessibility, SEO (Search Engine Optimization) and general best practices
- Used to (roughly) test the app on different devices
- Integrated into the CI pipeline
- Helped to pinpoint issues in the PWA (e.g. getting the 'install' prompt to appear etc.)
- Some issues are not relevant to our use case (e.g. SEO)

---
### Vite
![bg left](assets/slides/saw.jpg)

- Our replacement for the deprecated Create React App (CRA) boilerplate
- Fast, modern frontend build tool (leverages Rollup under the hood)
- Fast Hot Module Reloading (HMR) for development - changes are reflected in the browser almost instantly
- Out-of-the-box support for TypeScript, JSX, CSS and more

---
![bg right](assets/slides/road-issues.jpg)

### Challenges
- Modifying Indico's API to support the new app
- Building a new UI from scratch
- Learning curve for the team
- Deprecation of React CRA (Create React App) ➡️ Vite
- Browser/Device compatibility (especially Safari/Apple in general)

---
### Apple 💔 PWAs

<style scoped>
    section {
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        padding-bottom: 0 !important;
        padding-top: 0 !important;
    }

    h3 {
        font-size: 1.5em;
    }

    small {
        margin: 0;
        font-size: 0.8em;
        color: #aaa;
    }
</style>

![height:550px](assets/slides/apple-pwa-fuckery.png)

<small>Sources: The Register (Thomas C.) on [8 Feb. 2024](https://www.theregister.com/2024/02/08/apple_web_apps_eu/) and [16 Feb. 2024](https://www.theregister.com/2024/02/16/apple_web_apps/)</small>

---
### Apple ❤️‍🩹 PWAs

<style scoped>
    section {
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        padding-bottom: 0 !important;
        padding-top: 0 !important;
    }

    h3 {
        font-size: 1.5em;
    }

    small {
        margin: 0;
        font-size: 0.8em;
        color: #aaa;
    }
</style>

![height:500px](assets/slides/apple-pwa-uturn.png)

<small>Source: TechCrunch (Ivan M.) on [1 Mar. 2024](https://techcrunch.com/2024/03/01/apple-reverses-decision-about-blocking-web-apps-on-iphones-in-the-eu/)</small>

---
<!-- _backgroundColor: "#002939ff" -->
![bg right:50% width:60%](assets/theme/logo_indico_bw.svg)

### [🌐 getindico.io](https://getindico.io)
### ![checkin width:40px](assets/theme/checkin.png) [checkin.getindico.io](https://checkin.getindico.io)
### ![mastodon width:40px](assets/theme/mastodon.svg) [@getindico](https://fosstodon.org/@getindico)
### ![twitter width:40px](assets/theme/twitter.svg) [@getindico](https://twitter.com/getindico)
### ![matrix width:40px](assets/theme/matrix_bw.svg) [#indico:matrix.org](https://matrix.to/#/#indico:matrix.org)

<style scoped>
    p {
        text-align: middle;
    }

    img {
        vertical-align: middle;
    }

    a {
        color: #ffffff;
        text-decoration: none;
    }
</style>

---
<style scoped>
    section {
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }

    h3 {
        font-size: 1.5em;
    }

    small {
        font-size: 0.8em;
        color: #aaa;
    }
</style>

### 📷 Image sources disclaimer
Images used in this talk - apart from screenshots of the old and new check-in app, Indico/CERN logos/branding, social media logos, and press extracts from The Register and TechCrunch - are licensed under the [Unsplash License (longform below)](https://unsplash.com/license) and are free to use for commercial and non-commercial purposes.

> Unsplash grants you an irrevocable, nonexclusive, worldwide copyright license to download, copy, modify, distribute, perform, and use images from Unsplash for free, including for commercial purposes, without permission from or attributing the photographer or Unsplash. This license does not include the right to compile images from Unsplash to replicate a similar or competing service.

<small>Information correct at the time of writing (2nd May 2025)</small>
