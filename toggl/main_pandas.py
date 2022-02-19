# %%
import datetime
import json
from dataclasses import dataclass

import pandas as pd

from helpers import parse_time

@dataclass
class TogglEntry:
	description: str
	start: datetime
	end: datetime
	dur: int
	client: str
	project: str

	def __init__(self, entry: dict):
		self.description = entry['description']
		self.start = parse_time(entry['start'])
		self.end = parse_time(entry['end'])
		self.dur = int(entry['dur'] / 1000)
		self.client = entry['client']
		self.project = entry['project']

def duration_report(data: list[TogglEntry]):
	report = {}
	for d in data:
		if d.client not in report:
			report[d.client] = 0

		report[d.client] += d.dur
		
	report = {k: round(v/3600, 2) for k,v in report.items()}

	return report

# def filter_by_day(data: list[TogglEntry], day: datetime.date):
# 	for 

def sum_duration(data: list[TogglEntry]):
	duration = 0
	for d in data:
		duration += d.dur
	return duration

def get_last_week(df: pd.DataFrame):

	now = datetime.datetime.now()
	end_date = datetime.datetime.combine(now, datetime.time.max)
	tmp = datetime.datetime.combine(end_date, datetime.time.min)
	start_date = tmp - datetime.timedelta(days=6)

	mask = (df['start'] >= start_date) & (df['end'] < end_date)
	filtered = df.loc[mask]
	return filtered

def get_group_durations(df, group_name: str):
	grouped = df.groupby(group_name)
	total_dur = 0
	dur_seconds = {}

	for group in grouped.groups:
		dur = sum(grouped.get_group(group)['dur'])
		dur_seconds[group] = dur
		total_dur += dur

	dur_percentage = {k: round((v/ total_dur) * 100, 4) for k, v in dur_seconds.items()}

	return dur_seconds, dur_percentage


def main():
	with open('./data/2022-02-01.json') as f:
		data = json.load(f)

	df = pd.read_json('./data/2022-02-01.json')
	rows_to_delete = ['id', 'pid', 'tid', 'uid', 'billable', 'is_billable', 'cur',
										'tags', 'task', 'project_color']
	df.drop(rows_to_delete, axis=1, inplace=True)
	# df['start'] = df['start'].apply(lambda x: x.split('+')[0])
	# df['start'] = pd.to_datetime(df['start'], format='%Y-%m-%dT%H:%M:%S')
	df['start'] = df['start'].apply(parse_time)
	df['end'] = df['end'].apply(parse_time)
	df['dur'] = df['dur'].apply(lambda x: int(x/1000))

	last_week = get_last_week(df)

	dur_seconds, dur_percentage = get_group_durations(df, 'client')
	for k,v in dur_percentage.items():
		print(k, v)


if __name__ == '__main__':
	main()