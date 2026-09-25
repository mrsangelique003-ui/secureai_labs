"""
SecureAI Labs — Admin Dashboard
================================
Simple terminal dashboard to view all submissions.
Run: python admin.py
"""

import os
import json
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database')

COLLECTIONS = {
    '1': ('contacts',       'Contact Form Submissions'),
    '2': ('internships',    'Internship Applications'),
    '3': ('research_papers','Research Paper Submissions'),
    '4': ('video_entries',  'Video Challenge Entries'),
    '5': ('event_photos',   'Uploaded Event Photos'),
}

def load(collection):
    path = os.path.join(DB_DIR, f'{collection}.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return []

def print_header(title):
    print('\n' + '=' * 60)
    print(f'  {title}')
    print('=' * 60)

def show_contacts():
    records = load('contacts')
    print_header(f'Contact Submissions ({len(records)} total)')
    for r in records[-20:]:  # show last 20
        print(f"\n  [{r.get('id','')}] {r.get('created_at','')}")
        print(f"  Name:    {r.get('first_name','')} {r.get('last_name','')}")
        print(f"  Email:   {r.get('email','')}")
        print(f"  Type:    {r.get('inquiry_type','')}")
        print(f"  Message: {r.get('message','')[:80]}...")

def show_internships():
    records = load('internships')
    print_header(f'Internship Applications ({len(records)} total)')
    for r in records[-20:]:
        print(f"\n  [{r.get('id','')}] {r.get('created_at','')}")
        print(f"  Name:    {r.get('full_name','')}")
        print(f"  Email:   {r.get('email','')}")
        print(f"  Track:   {r.get('track','')}")
        print(f"  Level:   {r.get('level','')}")
        print(f"  Session: {r.get('session','')}")
        print(f"  Status:  {r.get('status','')}")

def show_research():
    records = load('research_papers')
    print_header(f'Research Submissions ({len(records)} total)')
    for r in records[-20:]:
        print(f"\n  [{r.get('id','')}] {r.get('created_at','')}")
        print(f"  Author:  {r.get('author_name','')}")
        print(f"  Email:   {r.get('email','')}")
        print(f"  Title:   {r.get('title','')[:60]}")
        print(f"  Area:    {r.get('research_area','')}")
        print(f"  Status:  {r.get('status','')}")

def show_video_entries():
    records = load('video_entries')
    print_header(f'Video Challenge Entries ({len(records)} total)')
    for r in records[-20:]:
        print(f"\n  [{r.get('id','')}] {r.get('created_at','')}")
        print(f"  Name:      {r.get('name','')}")
        print(f"  Instagram: {r.get('instagram','')}")
        print(f"  Phone:     {r.get('phone','')}")
        print(f"  Video URL: {r.get('video_url','')}")
        print(f"  Status:    {r.get('status','')}")

def show_stats():
    print_header('Dashboard Summary')
    total = 0
    for key, (col, label) in COLLECTIONS.items():
        count = len(load(col))
        total += count
        print(f"  {label:<35} {count:>5} records")
    print(f"\n  {'TOTAL':<35} {total:>5} records")
    print(f"\n  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def export_csv(collection, label):
    """Export a collection to CSV."""
    records = load(collection)
    if not records:
        print(f"  No records in {label}")
        return

    path = os.path.join(DB_DIR, f'{collection}.csv')
    headers = list(records[0].keys())

    with open(path, 'w', encoding='utf-8') as f:
        f.write(','.join(headers) + '\n')
        for r in records:
            row = [str(r.get(h, '')).replace(',', ';').replace('\n', ' ') for h in headers]
            f.write(','.join(row) + '\n')

    print(f"  Exported {len(records)} records to {path}")

def main():
    while True:
        print('\n' + '─' * 40)
        print('  SecureAI Labs Admin Dashboard')
        print('─' * 40)
        print('  1. View Contact Submissions')
        print('  2. View Internship Applications')
        print('  3. View Research Paper Submissions')
        print('  4. View Video Challenge Entries')
        print('  5. View Stats Summary')
        print('  6. Export All to CSV')
        print('  0. Exit')
        print('─' * 40)

        choice = input('  Choose: ').strip()

        if choice == '1':
            show_contacts()
        elif choice == '2':
            show_internships()
        elif choice == '3':
            show_research()
        elif choice == '4':
            show_video_entries()
        elif choice == '5':
            show_stats()
        elif choice == '6':
            for key, (col, label) in COLLECTIONS.items():
                export_csv(col, label)
        elif choice == '0':
            print('\n  Goodbye!\n')
            break
        else:
            print('  Invalid choice. Try again.')

if __name__ == '__main__':
    main()
