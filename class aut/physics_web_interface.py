#!/usr/bin/env python3
"""
Web Interface for Physics Avatar Teaching System
Provides a web-based control panel for generating physics videos
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
import json
import threading
from datetime import datetime
from physics_avatar_system import PhysicsAvatarSystem
import glob

app = Flask(__name__)
app.secret_key = 'physics-avatar-secret-key'

# Global system instance
physics_system = PhysicsAvatarSystem()
generation_status = {
    'is_running': False,
    'current_video': 0,
    'total_videos': 0,
    'current_topic': '',
    'progress_percentage': 0,
    'completed_videos': [],
    'errors': []
}

@app.route('/')
def dashboard():
    """Main dashboard showing curriculum overview"""
    summary = physics_system.get_curriculum_summary()
    
    # Get list of generated videos
    video_files = glob.glob("physics_lesson_*.mp4")
    videos = []
    for video_file in video_files:
        stat = os.stat(video_file)
        videos.append({
            'filename': video_file,
            'size_mb': round(stat.st_size / (1024*1024), 1),
            'created': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
        })
    
    return render_template('physics_dashboard.html', 
                         summary=summary, 
                         videos=videos,
                         status=generation_status)

@app.route('/curriculum')
def curriculum():
    """Show detailed curriculum"""
    return render_template('physics_curriculum.html', 
                         curriculum=physics_system.physics_curriculum)

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Video generation interface"""
    if request.method == 'POST':
        generation_type = request.form.get('type')
        
        if generation_type == 'all':
            return start_generation_all()
        elif generation_type == 'category':
            category = request.form.get('category')
            return start_generation_category(category)
        elif generation_type == 'single':
            category = request.form.get('category')
            lesson_index = int(request.form.get('lesson_index'))
            return start_generation_single(category, lesson_index)
    
    return render_template('physics_generate.html', 
                         curriculum=physics_system.physics_curriculum)

@app.route('/api/status')
def api_status():
    """API endpoint for generation status"""
    return jsonify(generation_status)

@app.route('/api/start_all')
def start_generation_all():
    """Start generating all physics videos"""
    if generation_status['is_running']:
        return jsonify({'error': 'Generation already in progress'})
    
    def generate_all():
        global generation_status
        generation_status['is_running'] = True
        generation_status['current_video'] = 0
        generation_status['total_videos'] = sum(len(lessons) for lessons in physics_system.physics_curriculum.values())
        generation_status['completed_videos'] = []
        generation_status['errors'] = []
        
        try:
            for category, lessons in physics_system.physics_curriculum.items():
                for i in range(len(lessons)):
                    if not generation_status['is_running']:  # Check for cancellation
                        break
                        
                    generation_status['current_video'] += 1
                    generation_status['current_topic'] = lessons[i]['topic']
                    generation_status['progress_percentage'] = int(
                        (generation_status['current_video'] / generation_status['total_videos']) * 100
                    )
                    
                    try:
                        video_file = physics_system.create_physics_video(category, i)
                        generation_status['completed_videos'].append({
                            'filename': video_file,
                            'topic': lessons[i]['topic'],
                            'category': category
                        })
                    except Exception as e:
                        generation_status['errors'].append({
                            'topic': lessons[i]['topic'],
                            'error': str(e)
                        })
        finally:
            generation_status['is_running'] = False
            generation_status['current_topic'] = 'Completed'
    
    thread = threading.Thread(target=generate_all)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'message': 'Generation started'})

@app.route('/api/start_category/<category>')
def start_generation_category(category):
    """Start generating videos for specific category"""
    if generation_status['is_running']:
        return jsonify({'error': 'Generation already in progress'})
    
    if category not in physics_system.physics_curriculum:
        return jsonify({'error': 'Invalid category'})
    
    def generate_category():
        global generation_status
        generation_status['is_running'] = True
        generation_status['current_video'] = 0
        generation_status['total_videos'] = len(physics_system.physics_curriculum[category])
        generation_status['completed_videos'] = []
        generation_status['errors'] = []
        
        try:
            lessons = physics_system.physics_curriculum[category]
            for i in range(len(lessons)):
                if not generation_status['is_running']:
                    break
                    
                generation_status['current_video'] += 1
                generation_status['current_topic'] = lessons[i]['topic']
                generation_status['progress_percentage'] = int(
                    (generation_status['current_video'] / generation_status['total_videos']) * 100
                )
                
                try:
                    video_file = physics_system.create_physics_video(category, i)
                    generation_status['completed_videos'].append({
                        'filename': video_file,
                        'topic': lessons[i]['topic'],
                        'category': category
                    })
                except Exception as e:
                    generation_status['errors'].append({
                        'topic': lessons[i]['topic'],
                        'error': str(e)
                    })
        finally:
            generation_status['is_running'] = False
            generation_status['current_topic'] = 'Completed'
    
    thread = threading.Thread(target=generate_category)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'message': f'Generation started for {category}'})

@app.route('/api/start_single/<category>/<int:lesson_index>')
def start_generation_single(category, lesson_index):
    """Start generating single video"""
    if generation_status['is_running']:
        return jsonify({'error': 'Generation already in progress'})
    
    if category not in physics_system.physics_curriculum:
        return jsonify({'error': 'Invalid category'})
    
    if lesson_index >= len(physics_system.physics_curriculum[category]):
        return jsonify({'error': 'Invalid lesson index'})
    
    def generate_single():
        global generation_status
        generation_status['is_running'] = True
        generation_status['current_video'] = 1
        generation_status['total_videos'] = 1
        generation_status['completed_videos'] = []
        generation_status['errors'] = []
        
        lesson = physics_system.physics_curriculum[category][lesson_index]
        generation_status['current_topic'] = lesson['topic']
        generation_status['progress_percentage'] = 50
        
        try:
            video_file = physics_system.create_physics_video(category, lesson_index)
            generation_status['completed_videos'].append({
                'filename': video_file,
                'topic': lesson['topic'],
                'category': category
            })
            generation_status['progress_percentage'] = 100
        except Exception as e:
            generation_status['errors'].append({
                'topic': lesson['topic'],
                'error': str(e)
            })
        finally:
            generation_status['is_running'] = False
            generation_status['current_topic'] = 'Completed'
    
    thread = threading.Thread(target=generate_single)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'message': 'Single video generation started'})

@app.route('/api/cancel')
def cancel_generation():
    """Cancel ongoing generation"""
    generation_status['is_running'] = False
    return jsonify({'success': True, 'message': 'Generation cancelled'})

@app.route('/download/<filename>')
def download_video(filename):
    """Download generated video"""
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return "File not found", 404

@app.route('/preview/<filename>')
def preview_video(filename):
    """Preview video in browser"""
    if os.path.exists(filename):
        return render_template('video_preview.html', filename=filename)
    return "File not found", 404

@app.route('/videos/<filename>')
def serve_video(filename):
    """Serve video file for preview"""
    if os.path.exists(filename):
        return send_file(filename)
    return "File not found", 404

if __name__ == '__main__':
    print("🔬 Physics Avatar Web Interface")
    print("🌐 Access at: http://localhost:5001")
    print("📱 Mobile access: http://[your-ip]:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)