# View.py for voter analytics
# 2026
# theodore harlan hpt@bu.edu
# 

from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Voter


import plotly.graph_objects as go
from plotly.offline import plot
from django.db.models import Count

# Create your views here.

class VoterListView(ListView):
    """
    Main paginated voter page with filtering options to
    make queries on the data from the csv which is now a voter model
    """
    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        qs = Voter.objects.all()

        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        if party:
            qs = qs.filter(party_affiliation=party)
        if min_dob:
            qs = qs.filter(date_of_birth__year__gte=min_dob)
        if max_dob:
            qs = qs.filter(date_of_birth__year__lte=max_dob)
        if score:
            qs = qs.filter(voter_score=score)
        if v20state:
            qs = qs.filter(v20state=True)
        if v21town:
            qs = qs.filter(v21town=True)
        if v21primary:
            qs = qs.filter(v21primary=True)
        if v22general:
            qs = qs.filter(v22general=True)
        if v23town:
            qs = qs.filter(v23town=True)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['parties'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        context['years'] = range(1900, 2025)
        context['scores'] = range(0, 6)

        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_dob'] = self.request.GET.get('min_dob', '')
        context['selected_max_dob'] = self.request.GET.get('max_dob', '')
        context['selected_score'] = self.request.GET.get('voter_score', '')
        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')
        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')

        return context

class VoterDetailView(DetailView):
    """
    Simple s ingle page for a voter
    """
    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'voter'
    



class VoterGraphsView(ListView):
    """
    page for graph view of voter data. pasted from voterlistview but
    also instead building the plotly plot from the querty with its filters
    """
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        qs = Voter.objects.all()

        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        if party:
            qs = qs.filter(party_affiliation=party)
        if min_dob:
            qs = qs.filter(date_of_birth__year__gte=min_dob)
        if max_dob:
            qs = qs.filter(date_of_birth__year__lte=max_dob)
        if score:
            qs = qs.filter(voter_score=score)
        if v20state:
            qs = qs.filter(v20state=True)
        if v21town:
            qs = qs.filter(v21town=True)
        if v21primary:
            qs = qs.filter(v21primary=True)
        if v22general:
            qs = qs.filter(v22general=True)
        if v23town:
            qs = qs.filter(v23town=True)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        context['parties'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        context['years'] = range(1900, 2025)
        context['scores'] = range(0, 6)
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_dob'] = self.request.GET.get('min_dob', '')
        context['selected_max_dob'] = self.request.GET.get('max_dob', '')
        context['selected_score'] = self.request.GET.get('voter_score', '')
        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')
        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')

        birth_years = qs.exclude(date_of_birth=None)\
                        .values('date_of_birth__year')\
                        .annotate(count=Count('id'))\
                        .order_by('date_of_birth__year') 
                        # get rid of the ones that were invalid from before
        #bar 
        fig1 = go.Figure(go.Bar(
            x=[b['date_of_birth__year'] for b in birth_years],
            y=[b['count'] for b in birth_years],
        ))
        fig1.update_layout(title='Voter Distribution by Birth Year', xaxis_title='Year', yaxis_title='Count')
        context['birth_year_graph'] = plot(fig1, output_type='div')

        parties = qs.values('party_affiliation')\
                    .annotate(count=Count('id'))\
                    .order_by('party_affiliation')
                    
                    
                    
                    
        #pie
        fig2 = go.Figure(go.Pie(
            labels=[p['party_affiliation'] for p in parties],
            values=[p['count'] for p in parties],
            hole=0.3,
            textposition='inside',
            textinfo='label+percent',
        ))
        
        fig2.update_layout(
            title='Voter Distribution by Party Affiliation',
            height=600,
            showlegend=True,
            )
        
        
        
        
        fig2.update_layout(title='Voter Distribution by Party Affiliation')
        context['party_graph'] = plot(fig2, output_type='div')


        elections = {
            'v20state': qs.filter(v20state=True).count(),
            'v21town': qs.filter(v21town=True).count(),
            'v21primary': qs.filter(v21primary=True).count(),
            'v22general': qs.filter(v22general=True).count(),
            'v23town': qs.filter(v23town=True).count(),
        }
        
        #chart
        fig3 = go.Figure(go.Bar(
            x=list(elections.keys()),
            y=list(elections.values()),
        ))
        fig3.update_layout(title='Voter Participation by Election', xaxis_title='Election', yaxis_title='Count')
        context['election_graph'] = plot(fig3, output_type='div')

        return context