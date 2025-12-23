#!/usr/bin/env python3
"""
Comprehensive Physics Avatar Teaching System
Generates automated physics video lessons with avatar for all major physics topics
"""

import os
import json
import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import pyttsx3
import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import *
import requests
from dataclasses import dataclass

@dataclass
class PhysicsLesson:
    topic: str
    category: str
    level: str  # beginner, intermediate, advanced
    content: str
    formulas: List[str]
    examples: List[str]
    duration_minutes: int

class PhysicsAvatarSystem:
    def __init__(self):
        self.physics_curriculum = self._load_comprehensive_physics_topics()
        self.avatar_config = {
            'voice_rate': 150,
            'voice_volume': 0.9,
            'avatar_style': 'professional',
            'background_color': '#1e3a8a',
            'text_color': 'white'
        }
        
    def _load_comprehensive_physics_topics(self) -> Dict[str, List[Dict]]:
        """Load comprehensive physics curriculum covering all major topics"""
        return {
            "mechanics": [
                {
                    "topic": "Kinematics - Motion in One Dimension",
                    "level": "beginner",
                    "content": "Study of motion without considering forces. Covers displacement, velocity, acceleration, and equations of motion.",
                    "formulas": ["v = u + at", "s = ut + ½at²", "v² = u² + 2as"],
                    "examples": ["Free fall", "Car acceleration", "Projectile motion"],
                    "duration": 8
                },
                {
                    "topic": "Newton's Laws of Motion",
                    "level": "beginner", 
                    "content": "Three fundamental laws governing motion: inertia, F=ma, and action-reaction pairs.",
                    "formulas": ["F = ma", "F₁₂ = -F₂₁"],
                    "examples": ["Pushing a box", "Rocket propulsion", "Walking"],
                    "duration": 10
                },
                {
                    "topic": "Work, Energy and Power",
                    "level": "intermediate",
                    "content": "Energy transformations, work-energy theorem, and power calculations in mechanical systems.",
                    "formulas": ["W = F·d·cos(θ)", "KE = ½mv²", "PE = mgh", "P = W/t"],
                    "examples": ["Lifting weights", "Roller coaster", "Hydroelectric power"],
                    "duration": 12
                },
                {
                    "topic": "Rotational Motion",
                    "level": "intermediate",
                    "content": "Angular motion, torque, moment of inertia, and rotational kinetic energy.",
                    "formulas": ["τ = rF sin(θ)", "I = Σmr²", "KE_rot = ½Iω²"],
                    "examples": ["Spinning wheel", "Figure skater", "Gyroscope"],
                    "duration": 15
                }
            ],
            "thermodynamics": [
                {
                    "topic": "Temperature and Heat",
                    "level": "beginner",
                    "content": "Temperature scales, thermal expansion, heat transfer mechanisms, and specific heat capacity.",
                    "formulas": ["Q = mcΔT", "ΔL = αL₀ΔT", "Q = kAΔT/d"],
                    "examples": ["Cooking food", "Thermal expansion of bridges", "Insulation"],
                    "duration": 10
                },
                {
                    "topic": "Laws of Thermodynamics",
                    "level": "advanced",
                    "content": "Four fundamental laws governing energy, entropy, and absolute zero temperature.",
                    "formulas": ["ΔU = Q - W", "ΔS ≥ 0", "η = 1 - T_c/T_h"],
                    "examples": ["Heat engines", "Refrigerators", "Carnot cycle"],
                    "duration": 18
                }
            ],
            "electromagnetism": [
                {
                    "topic": "Electric Fields and Forces",
                    "level": "beginner",
                    "content": "Coulomb's law, electric field strength, and electric potential energy.",
                    "formulas": ["F = kq₁q₂/r²", "E = F/q", "V = kq/r"],
                    "examples": ["Lightning", "Van de Graaff generator", "Capacitors"],
                    "duration": 12
                },
                {
                    "topic": "Magnetic Fields and Forces",
                    "level": "intermediate",
                    "content": "Magnetic field lines, Lorentz force, and electromagnetic induction.",
                    "formulas": ["F = qvB sin(θ)", "ε = -dΦ/dt", "B = μ₀I/2πr"],
                    "examples": ["MRI machines", "Electric motors", "Transformers"],
                    "duration": 14
                },
                {
                    "topic": "Maxwell's Equations",
                    "level": "advanced",
                    "content": "Four fundamental equations describing electromagnetic phenomena and wave propagation.",
                    "formulas": ["∇·E = ρ/ε₀", "∇×B = μ₀J + μ₀ε₀∂E/∂t"],
                    "examples": ["Radio waves", "Light propagation", "Electromagnetic spectrum"],
                    "duration": 20
                }
            ],
            "waves_optics": [
                {
                    "topic": "Wave Properties and Sound",
                    "level": "beginner",
                    "content": "Wave characteristics, sound waves, Doppler effect, and wave interference.",
                    "formulas": ["v = fλ", "f' = f(v±v_r)/(v±v_s)", "I ∝ A²"],
                    "examples": ["Musical instruments", "Ultrasound", "Noise cancellation"],
                    "duration": 11
                },
                {
                    "topic": "Geometric Optics",
                    "level": "intermediate",
                    "content": "Reflection, refraction, lenses, mirrors, and optical instruments.",
                    "formulas": ["n₁sin(θ₁) = n₂sin(θ₂)", "1/f = 1/d_o + 1/d_i"],
                    "examples": ["Eyeglasses", "Telescopes", "Fiber optics"],
                    "duration": 13
                },
                {
                    "topic": "Wave Optics and Interference",
                    "level": "advanced",
                    "content": "Wave nature of light, interference patterns, diffraction, and polarization.",
                    "formulas": ["d sin(θ) = mλ", "I = I₀ cos²(θ)"],
                    "examples": ["Double-slit experiment", "Holography", "LCD displays"],
                    "duration": 16
                }
            ],
            "modern_physics": [
                {
                    "topic": "Special Relativity",
                    "level": "advanced",
                    "content": "Time dilation, length contraction, mass-energy equivalence, and spacetime.",
                    "formulas": ["E = mc²", "γ = 1/√(1-v²/c²)", "Δt = γΔt₀"],
                    "examples": ["GPS satellites", "Particle accelerators", "Nuclear energy"],
                    "duration": 22
                },
                {
                    "topic": "Quantum Mechanics Basics",
                    "level": "advanced",
                    "content": "Wave-particle duality, uncertainty principle, and quantum states.",
                    "formulas": ["E = hf", "λ = h/p", "ΔxΔp ≥ ℏ/2"],
                    "examples": ["Photoelectric effect", "Electron microscopy", "Quantum computing"],
                    "duration": 25
                },
                {
                    "topic": "Nuclear Physics",
                    "level": "advanced",
                    "content": "Radioactive decay, nuclear reactions, binding energy, and applications.",
                    "formulas": ["N = N₀e^(-λt)", "E = Δmc²", "A = λN"],
                    "examples": ["Nuclear power", "Medical imaging", "Carbon dating"],
                    "duration": 18
                }
            ]
        }

    def create_enhanced_avatar(self, duration: float, topic: str) -> List[np.ndarray]:
        """Create enhanced animated avatar with physics-themed elements"""
        frames = []
        fps = 24
        total_frames = int(duration * fps)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor(self.avatar_config['background_color'])
        
        for frame in range(total_frames):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 8)
            ax.axis('off')
            ax.set_facecolor(self.avatar_config['background_color'])
            
            # Avatar head (animated)
            head_y = 6 + 0.1 * np.sin(frame * 0.2)  # Gentle bobbing
            head = plt.Circle((2, head_y), 0.8, color='#fbbf24', ec='#f59e0b', linewidth=2)
            ax.add_patch(head)
            
            # Eyes (blinking animation)
            if frame % 120 < 5:  # Blink every 5 seconds for 5 frames
                eye1 = plt.Rectangle((1.6, head_y-0.1), 0.2, 0.05, color='black')
                eye2 = plt.Rectangle((2.2, head_y-0.1), 0.2, 0.05, color='black')
            else:
                eye1 = plt.Circle((1.7, head_y), 0.1, color='white')
                eye2 = plt.Circle((2.3, head_y), 0.1, color='white')
                pupil1 = plt.Circle((1.7, head_y), 0.05, color='black')
                pupil2 = plt.Circle((2.3, head_y), 0.05, color='black')
                ax.add_patch(eye1)
                ax.add_patch(eye2)
                ax.add_patch(pupil1)
                ax.add_patch(pupil2)
            ax.add_patch(eye1)
            ax.add_patch(eye2)
            
            # Mouth (talking animation)
            mouth_height = 0.1 + 0.05 * np.sin(frame * 0.5)
            mouth = plt.Ellipse((2, head_y-0.4), 0.3, mouth_height, color='#dc2626')
            ax.add_patch(mouth)
            
            # Body
            body = plt.Rectangle((1.4, 3.5), 1.2, 2, color='#3b82f6', ec='#1d4ed8', linewidth=2)
            ax.add_patch(body)
            
            # Arms (gesturing)
            arm_angle = 15 * np.sin(frame * 0.1)
            # Left arm
            ax.plot([1.4, 0.8], [5, 4.5 + 0.3*np.sin(frame*0.1)], 'k-', linewidth=8, color='#fbbf24')
            # Right arm (pointing)
            ax.plot([2.6, 3.2], [5, 4.5 + 0.2*np.cos(frame*0.1)], 'k-', linewidth=8, color='#fbbf24')
            
            # Physics-themed background elements
            if 'mechanics' in topic.lower():
                # Draw trajectory
                x_traj = np.linspace(4, 9, 50)
                y_traj = 4 + 2*np.sin((x_traj-4)*0.5) * np.exp(-(x_traj-4)*0.2)
                ax.plot(x_traj, y_traj, '--', color='#10b981', linewidth=2, alpha=0.7)
                
            elif 'electric' in topic.lower() or 'magnetic' in topic.lower():
                # Draw field lines
                for i in range(3):
                    y_field = 2 + i * 1.5
                    ax.arrow(5, y_field, 2, 0, head_width=0.1, head_length=0.2, 
                            fc='#f59e0b', ec='#f59e0b', alpha=0.6)
                            
            elif 'wave' in topic.lower():
                # Draw wave
                x_wave = np.linspace(4, 9, 100)
                y_wave = 3 + 0.5 * np.sin(2*np.pi*(x_wave-4)/2 + frame*0.2)
                ax.plot(x_wave, y_wave, color='#8b5cf6', linewidth=3, alpha=0.8)
            
            # Topic title
            ax.text(5, 7.5, topic, fontsize=16, color=self.avatar_config['text_color'], 
                   ha='center', weight='bold', bbox=dict(boxstyle="round,pad=0.3", 
                   facecolor='rgba(0,0,0,0.7)', edgecolor='none'))
            
            # Convert to image array
            fig.canvas.draw()
            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            frames.append(image)
            
        plt.close(fig)
        return frames

    def generate_lesson_content(self, lesson_data: Dict) -> str:
        """Generate comprehensive lesson content with explanations and examples"""
        content = f"""
        Welcome to today's physics lesson on {lesson_data['topic']}.
        
        {lesson_data['content']}
        
        Let's explore the key formulas:
        """
        
        for i, formula in enumerate(lesson_data['formulas'], 1):
            content += f"\n{i}. {formula}"
            
        content += "\n\nNow let's look at real-world examples:"
        
        for i, example in enumerate(lesson_data['examples'], 1):
            content += f"\n{i}. {example}"
            
        content += f"""
        
        This concludes our {lesson_data['duration']}-minute lesson on {lesson_data['topic']}.
        Remember to practice these concepts and apply them to solve problems.
        Thank you for learning with us today!
        """
        
        return content

    def create_text_to_speech(self, text: str, filename: str = 'lesson_audio.wav'):
        """Generate high-quality text-to-speech audio"""
        engine = pyttsx3.init()
        
        # Configure voice settings
        voices = engine.getProperty('voices')
        if voices:
            # Try to use a female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        
        engine.setProperty('rate', self.avatar_config['voice_rate'])
        engine.setProperty('volume', self.avatar_config['voice_volume'])
        
        engine.save_to_file(text, filename)
        engine.runAndWait()
        return filename

    def create_physics_video(self, category: str, lesson_index: int) -> str:
        """Create a complete physics lesson video with avatar"""
        lesson_data = self.physics_curriculum[category][lesson_index]
        topic = lesson_data['topic']
        
        print(f"🎬 Creating video for: {topic}")
        
        # Generate lesson content
        lesson_content = self.generate_lesson_content(lesson_data)
        
        # Create audio
        audio_file = f"audio_{category}_{lesson_index}.wav"
        self.create_text_to_speech(lesson_content, audio_file)
        
        # Get audio duration
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        
        # Create avatar animation
        print("🎭 Generating avatar animation...")
        frames = self.create_enhanced_avatar(duration, topic)
        
        # Create video
        print("🎥 Assembling video...")
        video_clip = ImageSequenceClip(frames, fps=24)
        video_clip = video_clip.set_audio(audio_clip)
        
        # Add title screen
        title_clip = TextClip(f"Physics Lesson: {topic}", 
                             fontsize=50, color='white', bg_color='black')
        title_clip = title_clip.set_duration(3).set_position('center')
        
        # Combine clips
        final_video = concatenate_videoclips([title_clip, video_clip])
        
        # Output filename
        output_file = f"physics_lesson_{category}_{lesson_index}_{int(time.time())}.mp4"
        
        # Render video
        print("🔄 Rendering video...")
        final_video.write_videofile(output_file, fps=24, codec='libx264', 
                                   audio_codec='aac', temp_audiofile='temp-audio.m4a',
                                   remove_temp=True)
        
        # Cleanup
        os.remove(audio_file)
        audio_clip.close()
        video_clip.close()
        final_video.close()
        
        print(f"✅ Video created: {output_file}")
        return output_file

    def generate_all_physics_videos(self):
        """Generate videos for all physics topics"""
        print("🚀 Starting comprehensive physics video generation...")
        
        total_videos = sum(len(lessons) for lessons in self.physics_curriculum.values())
        current_video = 0
        
        for category, lessons in self.physics_curriculum.items():
            print(f"\n📚 Processing category: {category.upper()}")
            
            for i in range(len(lessons)):
                current_video += 1
                print(f"\n[{current_video}/{total_videos}] Creating lesson {i+1}/{len(lessons)}")
                
                try:
                    video_file = self.create_physics_video(category, i)
                    print(f"✅ Completed: {video_file}")
                    
                    # Optional: Add delay between videos to prevent system overload
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"❌ Error creating video for {lessons[i]['topic']}: {e}")
                    continue
        
        print(f"\n🎉 Completed generating {current_video} physics lesson videos!")

    def get_curriculum_summary(self) -> Dict:
        """Get a summary of the physics curriculum"""
        summary = {}
        total_duration = 0
        total_lessons = 0
        
        for category, lessons in self.physics_curriculum.items():
            category_duration = sum(lesson['duration'] for lesson in lessons)
            summary[category] = {
                'lesson_count': len(lessons),
                'total_duration_minutes': category_duration,
                'topics': [lesson['topic'] for lesson in lessons]
            }
            total_duration += category_duration
            total_lessons += len(lessons)
        
        summary['overall'] = {
            'total_lessons': total_lessons,
            'total_duration_hours': round(total_duration / 60, 1),
            'categories': list(self.physics_curriculum.keys())
        }
        
        return summary

def main():
    """Main function to run the physics avatar system"""
    system = PhysicsAvatarSystem()
    
    print("🔬 Physics Avatar Teaching System")
    print("=" * 50)
    
    # Show curriculum summary
    summary = system.get_curriculum_summary()
    print(f"📊 Curriculum Overview:")
    print(f"   Total Lessons: {summary['overall']['total_lessons']}")
    print(f"   Total Duration: {summary['overall']['total_duration_hours']} hours")
    print(f"   Categories: {', '.join(summary['overall']['categories'])}")
    
    print("\n🎬 Choose an option:")
    print("1. Generate all physics videos")
    print("2. Generate videos for specific category")
    print("3. Generate single lesson video")
    print("4. Show detailed curriculum")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        system.generate_all_physics_videos()
    elif choice == '2':
        print("\nAvailable categories:")
        for i, category in enumerate(system.physics_curriculum.keys(), 1):
            print(f"{i}. {category}")
        
        cat_choice = input("Select category number: ").strip()
        try:
            cat_index = int(cat_choice) - 1
            category = list(system.physics_curriculum.keys())[cat_index]
            
            for i in range(len(system.physics_curriculum[category])):
                system.create_physics_video(category, i)
        except (ValueError, IndexError):
            print("Invalid category selection")
    elif choice == '3':
        # Implementation for single lesson
        print("Single lesson generation - select category and lesson")
    elif choice == '4':
        print("\n📚 Detailed Curriculum:")
        for category, info in summary.items():
            if category != 'overall':
                print(f"\n{category.upper()}:")
                print(f"  Lessons: {info['lesson_count']}")
                print(f"  Duration: {info['total_duration_minutes']} minutes")
                for topic in info['topics']:
                    print(f"    • {topic}")

if __name__ == "__main__":
    main()