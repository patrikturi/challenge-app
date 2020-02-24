from django.shortcuts import render


# Last challange
def index(request):
    context = {
        'name': 'Last Challange Name',
        'start': None,
        'end': None,
        'teams': [
            {
                'id': 3,
                'name': 'TeamA',
                'calories': 123,
                'members': [
                    {
                        'name': 'Competitor 1',
                        'calories': 50
                    },
                    {
                        'name': 'Competitor 2',
                        'calories': 73
                    }
                ]
            },
            {
                'id': 5,
                'name': 'TeamB',
                'calories': 10,
                'members': [
                    {
                        'name': 'Competitor 3',
                        'calories': 10
                    }
                ]
            }
        ]
    }
    return render(request, 'index.html', context)
