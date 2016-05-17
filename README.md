# slack-post

## Prerequisites

- Python3
- Additional packages (See below)

```
$ pip install neovim
```

```
$ pip install slackclient
```

## Installation

In case you use vim-plug:

```vim
function! DoRemote(arg)
  UpdateRemotePlugins
endfunction

Plug '5t111111/slack-post.nvim', { 'do': function('DoRemote') }
```

## Configuration

The following global var should be set in Neovim configuration:

- g:slack_api_token : slack api token (See https://api.slack.com/web for details)
- g:slack_channel_to_post : slack channel you want to post to
- g:slack_username : slack username (optional)
- g:slack_icon_emoji : slack emoji for icon (optional)

## Commands

```
:PostTextToSlack
```

```
:PostCodeToSlack
```
