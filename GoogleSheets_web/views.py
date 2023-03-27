from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

@login_required
def index(request):
    if not request.user.social_auth.exists():
        return render(request, 'my_app/error.html', {'error_message': 'Google account not connected.'})

    social_auth = request.user.social_auth.get(provider='google')
    credentials = Credentials.from_authorized_user_info(info=social_auth.extra_data)
    sheets = build('sheets', 'v4', credentials=credentials)

    sheet_ids = ['sheet_id_1', 'sheet_id_2']
    sheet_data = []

    for sheet_id in sheet_ids:
        result = sheets.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range='A1:Z100'
        ).execute()

        sheet_data.append(result.get('values', []))

    return render(request, 'my_app/index.html', {'sheets': sheet_data})
