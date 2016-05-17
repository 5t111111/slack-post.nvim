import neovim
from slackclient import SlackClient

@neovim.plugin
class SlackPost(object):
    """
    the following global var should be set in Neovim configuration
    - g:slack_api_token : slack api token
    - g:slack_channel_to_post : slack channel you want to post to
    - g:slack_username : slack username (optional)
    - g:slack_icon_emoji : slack emoji for icon (optional)
    """
    def __init__(self, nvim):
        self.nvim = nvim
        self.text = None

    @neovim.command("PostTextToSlack", range='')
    def post_text_to_slack(self, range):
        b = self.nvim.current.buffer
        lines = b[(range[0]-1):range[1]]
        self.text = "\n".join(lines)

        return self.__execute_posting()
    
    @neovim.command("PostCodeToSlack", range='')
    def post_code_to_slack(self, range):
        b = self.nvim.current.buffer
        lines = b[(range[0]-1):range[1]]
        lines.insert(0, '```')
        lines.append('```')
        self.text = "\n".join(lines)

        return self.__execute_posting()

    def __execute_posting(self):
        token = self.__get_vim_global_var_safely('slack_api_token')
        if not token:
            return False

        channel = self.__get_vim_global_var_safely('slack_channel_to_post')
        if not channel:
            return False

        username = self.__get_vim_global_var_safely('slack_username')
        if not username:
            username = 'Nvim Bot'

        icon_emoji = self.__get_vim_global_var_safely('slack_icon_emoji')
        if not icon_emoji:
            icon_emoji = ':robot_face:'

        self.nvim.command(':let choice = confirm("Are you sure you want to post the selected lines to Slack?", "y Yes\nn No\n")')
        answer = self.nvim.eval('choice')

        if answer == 1:
            sc = SlackClient(token)

            sc.api_call(
                'chat.postMessage',
                channel=channel,
                text=self.text,
                username=username,
                icon_emoji=icon_emoji
            )

            self.nvim.command('echo "Posted!"')
            return True
        else:
            self.nvim.command('echo "Canceled"')
            return False

    def __get_vim_global_var_safely(self, var_name):
        self.nvim.command(':let g:{var_name!s} = get(g:, "{var_name!s}", "")'.format(**locals()))
        value = self.nvim.eval('g:{var_name!s}'.format(**locals()))
    
        if not value:
            self.nvim.err_write("g:{var_name!s} is not set\n".format(**locals()))
            return False

        return value
