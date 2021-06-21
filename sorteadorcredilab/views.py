from sorteadorcredilab.sorteador.models import Participante
from slack import WebClient
from rest_framework.response import Response
from rest_framework import views, status


class NotificacaoViewSet(views.APIView):

    @classmethod
    def get_extra_actions(cls):
        return []

    def post(self, request):
        try:
            slack_web_client = WebClient(
            'xoxb-460405341186-2098420383619-ry83YkTrCuULS737hOIVlxAT')

            data = request.data.get('data')
            facilitador: Participante = Participante.objects.get(id=request.data.get('facilitador'))
            secretario: Participante = Participante.objects.get(id=request.data.get('secretario'))

            channel_id = ''
            channels = slack_web_client.conversations_list()
            for channel in channels['channels']:
                if channel['is_member']:
                    channel_id = channel['id']

                    if channel_id:
                        message = {
                            "channel": channel_id,
                            "link_names": True,
                            "parse": "full",
                            "blocks": [
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": f"Sorteados para a diária do dia { data[8:] }/{ data[5:7] }/{ data[:4] } :tada:"
                                    }
                                },
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": f"*Facilitador*: <@{ self.get_user_by_username(slack_web_client, facilitador.nome_slack) }>"
                                    },
                                    "accessory": {
                                        "type": "image",
                                        "image_url": f"https://softfocus.com.br/avatares/{ facilitador.avatar }.jpg",
                                        "alt_text": facilitador.nome
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": f"*Secretário*: <@{ self.get_user_by_username(slack_web_client, secretario.nome_slack) }>"
                                    },
                                    "accessory": {
                                        "type": "image",
                                        "image_url": f"https://softfocus.com.br/avatares/{ secretario.avatar }.jpg",
                                        "alt_text": secretario.nome
                                    }
                                }
                            ]
                        }

                        slack_web_client.chat_postMessage(**message)
            return Response(True, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get_user_by_username(self, slack_web_client, username):
        users = slack_web_client.users_list()

        for user in users.data.get('members'):
            if user.get('profile').get('display_name') == username or user.get('profile').get('real_name') == username:
                return user.get('id')

