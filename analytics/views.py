from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime
from activities.models import Activity
from .utils import get_period_dates, calculate_streak

class SummaryAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        period = request.query_params.get('period', 'week')
        date_str = request.query_params.get('date')
        
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = timezone.now().date()
        
        start_date, end_date = get_period_dates(period, date)
        
        activities = Activity.objects.filter(
            sub_branch__branch__domain__user=request.user,
            date__gte=start_date,
            date__lte=end_date
        )
        
        stats = activities.aggregate(
            total_duration=Sum('duration'),
            total_activities=Count('id')
        )
        
        # Calculate average daily duration
        days_in_period = (end_date - start_date).days + 1
        avg_daily = stats['total_duration'] / days_in_period if stats['total_duration'] else 0
        
        # Domain breakdown
        domain_stats = activities.values(
            'sub_branch__branch__domain__id',
            'sub_branch__branch__domain__name'
        ).annotate(
            duration=Sum('duration')
        ).order_by('-duration')
        
        total = stats['total_duration'] or 1
        domains_data = [
            {
                'domain_id': d['sub_branch__branch__domain__id'],
                'domain_name': d['sub_branch__branch__domain__name'],
                'duration': d['duration'],
                'percentage': round((d['duration'] / total) * 100, 2)
            }
            for d in domain_stats
        ]

        # Branch breakdown
        branch_stats = activities.values(
            'sub_branch__branch__id',
            'sub_branch__branch__name'
        ).annotate(
            duration=Sum('duration')
        ).order_by('-duration')

        branches_data = [
            {
                'branch_id': b['sub_branch__branch__id'],
                'branch_name': b['sub_branch__branch__name'],
                'duration': b['duration'],
                'percentage': round((b['duration'] / total) * 100, 2)
            }
            for b in branch_stats
        ]

        # Sub-branch breakdown
        subbranch_stats = activities.values(
            'sub_branch__id',
            'sub_branch__name'
        ).annotate(
            duration=Sum('duration')
        ).order_by('-duration')

        sub_branches_data = [
            {
                'sub_branch_id': s['sub_branch__id'],
                'sub_branch_name': s['sub_branch__name'],
                'duration': s['duration'],
                'percentage': round((s['duration'] / total) * 100, 2)
            }
            for s in subbranch_stats
        ]

        # Topic breakdown
        topic_stats = activities.values(
            'topics__id',
            'topics__name'
        ).annotate(
            duration=Sum('duration')
        ).order_by('-duration')

        topics_data = [
            {
                'topic_id': t['topics__id'],
                'topic_name': t['topics__name'],
                'duration': t['duration'],
                'percentage': round((t['duration'] / total) * 100, 2)
            }
            for t in topic_stats if t['topics__id'] is not None
        ]

        # Weekday stats (for "Most Productive Day")
        weekday_stats = activities.values('day').annotate(
            duration=Sum('duration'),
            count=Count('id')
        ).order_by('-duration')

        # Time of day stats (for "Prime Session Time")
        # Categorize by hour: Morning (5-11), Afternoon (12-16), Evening (17-21), Night (22-4)
        time_stats = {
            'Morning (5AM-12PM)': 0,
            'Afternoon (12PM-5PM)': 0,
            'Evening (5PM-10PM)': 0,
            'Night (10PM-5AM)': 0
        }
        
        for activity in activities.filter(time__isnull=False):
            hour = activity.time.hour
            if 5 <= hour < 12:
                time_stats['Morning (5AM-12PM)'] += activity.duration
            elif 12 <= hour < 17:
                time_stats['Afternoon (12PM-5PM)'] += activity.duration
            elif 17 <= hour < 22:
                time_stats['Evening (5PM-10PM)'] += activity.duration
            else:
                time_stats['Night (10PM-5AM)'] += activity.duration

        time_of_day_data = [
            {'category': k, 'duration': v, 'percentage': round((v / total) * 100, 2)}
            for k, v in time_stats.items() if v > 0
        ]
        time_of_day_data.sort(key=lambda x: x['duration'], reverse=True)
        
        return Response({
            'period': period,
            'start_date': start_date,
            'end_date': end_date,
            'total_duration': stats['total_duration'] or 0,
            'total_activities': stats['total_activities'] or 0,
            'average_daily_duration': round(avg_daily, 2),
            'domains': domains_data,
            'branches': branches_data,
            'sub_branches': sub_branches_data,
            'topics': topics_data,
            'weekdays': list(weekday_stats),
            'time_of_day': time_of_day_data
        })

class DomainAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        activities = Activity.objects.filter(
            sub_branch__branch__domain__user=request.user
        )
        
        if date_from:
            activities = activities.filter(date__gte=date_from)
        if date_to:
            activities = activities.filter(date__lte=date_to)
        
        # Group by domain, then branch, then sub-branch
        domain_data = {}
        
        for activity in activities:
            domain = activity.sub_branch.branch.domain
            branch = activity.sub_branch.branch
            sub_branch = activity.sub_branch
            
            if domain.id not in domain_data:
                domain_data[domain.id] = {
                    'domain_id': domain.id,
                    'domain_name': domain.name,
                    'total_duration': 0,
                    'branches': {}
                }
            
            if branch.id not in domain_data[domain.id]['branches']:
                domain_data[domain.id]['branches'][branch.id] = {
                    'branch_id': branch.id,
                    'branch_name': branch.name,
                    'duration': 0,
                    'sub_branches': {}
                }
            
            if sub_branch.id not in domain_data[domain.id]['branches'][branch.id]['sub_branches']:
                domain_data[domain.id]['branches'][branch.id]['sub_branches'][sub_branch.id] = {
                    'sub_branch_id': sub_branch.id,
                    'sub_branch_name': sub_branch.name,
                    'duration': 0
                }
            
            domain_data[domain.id]['total_duration'] += activity.duration
            domain_data[domain.id]['branches'][branch.id]['duration'] += activity.duration
            domain_data[domain.id]['branches'][branch.id]['sub_branches'][sub_branch.id]['duration'] += activity.duration
        
        # Convert to list format
        result = []
        for domain in domain_data.values():
            domain['branches'] = [
                {
                    **branch,
                    'sub_branches': list(branch['sub_branches'].values())
                }
                for branch in domain['branches'].values()
            ]
            result.append(domain)
        
        return Response(result)

class BranchAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        domain_id = request.query_params.get('domain')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        activities = Activity.objects.filter(
            sub_branch__branch__domain__user=request.user
        )
        
        if domain_id:
            activities = activities.filter(sub_branch__branch__domain_id=domain_id)
        if date_from:
            activities = activities.filter(date__gte=date_from)
        if date_to:
            activities = activities.filter(date__lte=date_to)
        
        branch_stats = activities.values(
            'sub_branch__branch__id',
            'sub_branch__branch__name'
        ).annotate(
            total_duration=Sum('duration'),
            activities_count=Count('id')
        ).order_by('-total_duration')
        
        result = [
            {
                'branch_id': b['sub_branch__branch__id'],
                'branch_name': b['sub_branch__branch__name'],
                'total_duration': b['total_duration'],
                'activities_count': b['activities_count']
            }
            for b in branch_stats
        ]
        
        return Response(result)

class SubBranchAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        branch_id = request.query_params.get('branch')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        activities = Activity.objects.filter(
            sub_branch__branch__domain__user=request.user
        )
        
        if branch_id:
            activities = activities.filter(sub_branch__branch_id=branch_id)
        if date_from:
            activities = activities.filter(date__gte=date_from)
        if date_to:
            activities = activities.filter(date__lte=date_to)
        
        subbranch_stats = activities.values(
            'sub_branch__id',
            'sub_branch__name'
        ).annotate(
            total_duration=Sum('duration'),
            activities_count=Count('id')
        ).order_by('-total_duration')
        
        result = [
            {
                'sub_branch_id': s['sub_branch__id'],
                'sub_branch_name': s['sub_branch__name'],
                'total_duration': s['total_duration'],
                'activities_count': s['activities_count']
            }
            for s in subbranch_stats
        ]
        
        return Response(result)

class DailyAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        breakdown_type = request.query_params.get('type')  # domain, branch, sub_branch
        ids_str = request.query_params.get('ids')
        
        activities = Activity.objects.filter(
            sub_branch__branch__domain__user=request.user
        )
        
        if date_from:
            activities = activities.filter(date__gte=date_from)
        if date_to:
            activities = activities.filter(date__lte=date_to)

        # 1. Get total duration per day
        daily_totals = activities.values('date').annotate(
            Total=Sum('duration')
        ).order_by('date')
        
        pivoted = {d['date'].strftime('%Y-%m-%d'): {'date': d['date'].strftime('%Y-%m-%d'), 'Total': d['Total']} for d in daily_totals}

        # 2. If breakdown requested, fetch durations for specific IDs
        if breakdown_type and ids_str:
            ids = [int(i) for i in ids_str.split(',') if i.strip()]
            
            if breakdown_type == 'domain':
                field = 'sub_branch__branch__domain_id'
                name_field = 'sub_branch__branch__domain__name'
            elif breakdown_type == 'branch':
                field = 'sub_branch__branch_id'
                name_field = 'sub_branch__branch__name'
            else:
                field = 'sub_branch_id'
                name_field = 'sub_branch__name'

            breakdown_stats = activities.filter(**{f"{field}__in": ids}).values('date', field, name_field).annotate(
                duration=Sum('duration')
            ).order_by('date')

            for s in breakdown_stats:
                dt_key = s['date'].strftime('%Y-%m-%d')
                if dt_key in pivoted:
                    pivoted[dt_key][f'id_{s[field]}'] = s['duration']
                    pivoted[dt_key][f'name_{s[field]}'] = s[name_field]

        return Response(sorted(pivoted.values(), key=lambda x: x['date']))

class StreakAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        activities = Activity.objects.filter(
            sub_branch__branch__domain__user=request.user
        ).order_by('-date')
        
        streak_data = calculate_streak(activities)
        
        return Response(streak_data)

class TopicDetailedAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        sub_branch_ids = request.query_params.get('sub_branch_ids')
        
        from curriculum.models import Topic
        topics = Topic.objects.filter(sub_branch__branch__domain__user=request.user)
        
        if sub_branch_ids:
            ids = [int(i) for i in sub_branch_ids.split(',') if i.strip()]
            topics = topics.filter(sub_branch_id__in=ids)
            
        # Get total duration per topic
        topic_stats = topics.annotate(
            total_duration=Sum('activities__duration')
        ).values('id', 'name', 'created_at', 'total_duration', 'sub_branch__name')
        
        result = [
            {
                'id': t['id'],
                'name': t['name'],
                'total_duration': t['total_duration'] or 0,
                'created_at': t['created_at'],
                'sub_branch_name': t['sub_branch__name']
            }
            for t in topic_stats
        ]
        
        return Response(result)
