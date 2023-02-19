<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/DefNotAvg/DNABot">
    <img src="https://avatars.githubusercontent.com/u/26437025?v=4" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">DNABot</h3>

  <p align="center">
    Discord Bot for the <a href="https://discord.gg/4tkd2Z9Dp4" target="_blank">DefNotAvg Community server</a>.
    <br />
    <br />
    <a href="https://github.com/DefNotAvg/DNABot/issues">Report Bug</a>
    ·
    <a href="https://github.com/DefNotAvg/DNABot/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

* pip
  ```sh
  pip install -r requirements.txt
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/DefNotAvg/DNABot.git
   ```
2. Install Python packages
   ```sh
   pip install -r requirements.txt
   ```
3. Set your Discord bot token as the `discordToken` environment variable ([reference doc](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html))

4. Edit config.json to your liking
   ```sh
   {
    "enableForwarding": true, # Required | boolean | true to send messages to privateChannelId, requiring manual approval to send to publicChannelId; false to send all messages to publicChannelId
    "publicChannelId": 12345, # Required | int | channelId to send all messages to if enableForwarding is set to false; if enableForwarding is set to true, manual intervention is needed to send messages from privateChannelId to publicChannelId
    "privateChannelId": 12345, # Optional | int | channelId to send all messages to if enableForwarding is set to true
   }
   ```
5. Run main.py

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Add monitoring for fitness-related deals on popular supplements/items
- [ ] Add message forwarding capabilities so that all messages don't need to be visible to all users

See the [open issues](https://github.com/DefNotAvg/DNABot/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Dante Arcese - [@DefNotAvg](https://twitter.com/DefNotAvg) - DefNotAvg@gmail.com

Project Link: [https://github.com/DefNotAvg/DNABot](https://github.com/DefNotAvg/DNABot)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/DefNotAvg/DNABot.svg?style=for-the-badge
[contributors-url]: https://github.com/DefNotAvg/DNABot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/DefNotAvg/DNABot.svg?style=for-the-badge
[forks-url]: https://github.com/DefNotAvg/DNABot/network/members
[stars-shield]: https://img.shields.io/github/stars/DefNotAvg/DNABot.svg?style=for-the-badge
[stars-url]: https://github.com/DefNotAvg/DNABot/stargazers
[issues-shield]: https://img.shields.io/github/issues/DefNotAvg/DNABot.svg?style=for-the-badge
[issues-url]: https://github.com/DefNotAvg/DNABot/issues