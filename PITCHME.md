---
marp: true
title: "Using LLMs: Summarization of meeting minutes in Indico"
theme: default
paginate: true
_paginate: false
footer: ''
---
<!-- _footer: '' -->

![](assets/theme/cern_bw.svg)

<style scoped>
    section {
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        background-color: #0033A0 !important;
    }

    img {
        width: 200px !important;
        height: 200px !important;
    }
</style>

---
<!-- _paginate: false -->
![width:400px right:50% left:50%](assets/theme/logo.svg)
*Using LLMs: Summarization of meeting minutes in Indico*

### Dominic Hollis & Tomas Roun - Indico Team
### IT-CA Group Meeting - 21st Oct. 2025

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
<!-- _paginate: false -->
![bg right](assets/slides/clocks.jpg)

### The current problem

 - Users are compiling meeting minutes in Indico (great!)
 - ...just to send it to another meeting
 - Manually extracting relevant minutes is tedious
 - Trying to get a summary of the minutes is time-consuming

---
<!-- _paginate: false -->
![bg right](assets/slides/monkey.jpg)

### What can we do about it?

---
<!-- _paginate: false -->
![bg right](assets/slides/monkey.jpg)

### What can we do about it?

 - Abolish meetings? (not likely)

---
<!-- _paginate: false -->
![bg right](assets/slides/monkey.jpg)

### What can we do about it?

 - Abolish meetings? (not likely)
 - Hire more staff? (expensive)

---
<!-- _paginate: false -->
![bg right](assets/slides/monkey.jpg)

### What can we do about it?

 - Abolish meetings? (not likely)
 - Hire more staff? (expensive)
 - Use Large Language Models (LLMs) to summarize minutes? (interesting...)

---
<!-- _paginate: false -->
![bg right](assets/slides/monkey.jpg)

### What can we do about it?

 - Abolish meetings? (not likely)
 - Hire more staff? (expensive)
 - Use Large Language Models (LLMs) to summarize minutes? (interesting...)
 - Use emails instead? (nope)

---
<!-- _paginate: false -->
![bg right](assets/slides/monkey.jpg)

<style scoped>
    .muted {
        color: #dbdbdb !important;
        font-style: italic !important;
    }
</style>

### What can we do about it?

 - <span class="muted">~~Abolish meetings? (not likely)~~</span>
 - <span class="muted">~~Hire more staff? (expensive)~~</span>
 - <strong>✅ Use Large Language Models (LLMs) to summarize minutes? (interesting...)</strong>
 - <span class="muted">~~Use emails instead? (nope)~~</span>

---
<!-- _paginate: false -->
![bg right](assets/slides/layers.jpg)
### Why LLMs?
- Powerful text processing capabilities
- Can generate human-like summaries
- Can be integrated into existing workflows
- Potential to save time and effort for users
---
<!-- _paginate: false -->
![bg right](assets/slides/planning.jpg)
### Summer student project
- Idea proposed in early 2025
- Summer student: Zeynep Çaysar
- Masters A.I. student @ UZH
- Developed a prototype summarization feature
- Integrated with Indico's meeting minutes system
---
<!-- _paginate: false -->
<style scoped>
    section {
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        padding-bottom: 0 !important;
        padding-top: 0 !important;
    }

    h1 {
        font-size: 5em;
    }
</style>

# Demo
---
<!-- _paginate: false -->
### Overview

![height:250px](assets/slides/diagram.png)

<style scoped>
    section {
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        padding-bottom: 0 !important;
        padding-top: 0 !important;
    }

    h3 {
        font-size: 2em;
    }

    img {
        margin-top: 70px;
        margin-bottom: 70px;
    }
</style>

---
<!-- _paginate: false -->
![bg right](assets/slides/gears.jpg)
### Future work
- Get this on prod by late 2025/early 2026
- Tweak mode (take a generated summary and ask for modifications)
- Maybe something else? 🤔

---
<!-- _backgroundColor: "#002939ff" -->
<!-- _paginate: false -->
![bg right:50% width:60%](assets/theme/logo_indico_bw.svg)

### 🌐 [getindico.io](https://getindico.io)
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
<!-- _paginate: false -->
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
Images used in this talk - apart from Indico/CERN logos/branding, social media logos - are licensed under the [Unsplash License (longform below)](https://unsplash.com/license) and are free to use for commercial and non-commercial purposes.

> Unsplash grants you an irrevocable, nonexclusive, worldwide copyright license to download, copy, modify, distribute, perform, and use images from Unsplash for free, including for commercial purposes, without permission from or attributing the photographer or Unsplash. This license does not include the right to compile images from Unsplash to replicate a similar or competing service.

<small>Information correct at the time of writing (17th October 2025)</small>
