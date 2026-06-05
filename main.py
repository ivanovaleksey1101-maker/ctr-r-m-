# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Original project: Classic Text RPG - Retro (Music)
# Original repository: https://github.com/ivanovaleksey1101-maker/ctr-r-m-.git
import vlc
import pygame
import time
import random
import json
import sys

# Fix for Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

pygame.mixer.init()

class Media:
    """Music & Sounds Playing Tools"""
    def __init__(self):
        self.sounds = {"atack": ['atack1', 'atack2'], 'heal': ['heal'], 'crit': ['crit']} # category: [sound1, sound2]
        self.musics = ['life_of_traveler', 'explore', 'fight']
        self.original_volume = 1.0 
    
    def intro(self):
        """My Intro"""
        player = vlc.MediaPlayer("intro.mp4")
        player.play()
        time.sleep(10)
        player.stop()
    
    def music(self, num: int):
        """Background music"""
        pygame.mixer.music.load(f'music/{self.musics[num]}.ogg')
        pygame.mixer.music.set_volume(self.original_volume)  # Set orginal volume
        pygame.mixer.music.play(-1)
    
    def set_music_volume(self, volume: float):
        """Установить громкость музыки (0.0 - 1.0)"""
        pygame.mixer.music.set_volume(volume)
    
    def sound(self, val):
        """One random sound from category with music ducking"""
        # Reduce volume
        self.set_music_volume(0.2)
        
        # Play sound
        sound = pygame.mixer.Sound(f'sounds/{random.choice(self.sounds[val])}.ogg')
        sound.play()
        
        # Wait sound ending
        wait_time = sound.get_length()
        time.sleep(wait_time)
        
        # Return volume
        self.set_music_volume(self.original_volume)

class Game:
    def __init__(self, language="en"):
        # load language
        self.l = {}
        with open(f'languages/{language}.json', 'r', encoding='utf-8') as file:
            self.l = json.load(file)
        
        # Game status and information
        self.main_event = "cave" # locations: cave, floor is lava, dark cave
        self.event = "normal" # local difficult: easy, normal, hard
        self.m = Media()
        self.steps = 0
        self.mobs = {
            'cave': [
                ["Goblin", 10, 2, 6, 4],
                ["Raider", 14, 3, 4, 6],
                ["Mouse", 6, 0, 8, 1]
            ],
            
            'dark cave': [
                ["BIG Mouse", 18, 4, 8, 8],
                ["Monster", 16, 6, 10, 12]
            ],
            
            'floor is lava': [
                ["Lava Monster", 22, 8, 12, 14]
            ]
        }
        
        # Player stats
        self.name = None # player name
        self.level = 1
        self.exp = 0
        self.player = {'hp': 20, 'hp_max': 20, 'arm': 1, 'dmg': 5} # main stats
        self.gold = 20 # money
    
    def choice(self, choices):
        """System Choice"""
        lens = len(choices)
        
        print(self.l['choice'])
        for i in range(lens):
            print(f"{i+1}. {choices[i]}")
        
        answer = input(" >>> ")
        
        if answer in [str(num+1) for num in range(lens)]:
            return answer
        else:
            return False
    
    def play(self):
        m.music(0)
        is_sure = False
        while not is_sure:
            print(self.l['enter_name'])
            name = input(self.l['my_name'])
            print(f"{self.l['remember_name']}, {name}? (Y/N)")
            answer = input()
            if answer.lower() == 'y':
                is_sure = True
                self.name = name
        
        m.music(1)
        while True:
            # choice for player
            anw = self.choice([self.l['explore'], self.l['rest'], self.l['stats'], self.l['leave']])
            
            if not anw:
                print(self.l['wrong_choice'])
            elif anw == '1':
                self.gameloop()
            elif anw == '2':
                self.rest()
            elif anw == '3':
                self.show_stats()
                input(self.l['press_enter'])
            elif anw == '4':
                self.m.music(0)
                print(self.l['exit_game'], "(Y/N)")
                answer = input()
                if answer.lower() == 'y':
                    break
                else:
                    self.m.music(1)
    
    def show_stats(self):
        """Show stats player in game"""
        print(self.l['level'], self.level, f"({self.exp}/{self.max_exp()})")
        print(f"{self.l['hp']}: {self.player['hp']}/{self.player['hp_max']}. {self.l['armor']}: {self.player['arm']}. {self.l['damage']}: {self.player['dmg']}.")
        print(f"{self.l['gold']}:", self.gold)
    
    def gameloop(self):
        while True:
            print(self.l['you_go'])
            time.sleep(2)
            self.steps += 1
            self.m.music(2)
            mob = random.choice(self.mobs[self.main_event]).copy()
            self.fight(mob)
            
            if self.steps == 3:
                self.steps = 0
                self.main_event = random.choice(['cave', 'floor is lava', 'dark cave'])
                print(f"{self.l['new_location']} '{self.main_event}'!")
            
            print(self.l['continue_quest'], "(Y/N)")
            answer = input()
            if answer.lower() != 'y':
                print(self.l['stay_here'])
                m.music(1)
                break
    
    def fight(self, mob):
        enemy = mob
        while True:
            print(f'\n{self.name} {self.player["hp"]}/{self.player["hp_max"]} hp | VS | {enemy[0]} {enemy[1]} hp')
            do = self.choice([self.l['attack'], self.l['heal'], self.l['run']])
            print()
            
            # === TURN PLAYER ===
            if not do:
                print(self.l['wrong_choice'])
                continue
            elif do == '1':
                if random.random() < 0.2: # CRIT
                    dmg = self.player["dmg"]*2 - enemy[2]
                    print(f"{self.l['critical_hit']} ({dmg} {self.l['damage_dealt']})!!!")
                    enemy[1] -= dmg
                    self.m.sound('crit')
                else:
                    if self.event == 'easy':
                        dmg = self.player["dmg"] - enemy[2] - random.randint(0, 2)
                    elif self.event == 'normal':
                        dmg = self.player["dmg"] - enemy[2] - random.randint(-1, 1)
                    elif self.event == 'hard':
                        dmg = self.player["dmg"] - enemy[2] - random.randint(-2, 0)
                    
                    if dmg > 0:
                        print(f"{self.l['hit']} {dmg} {self.l['damage_dealt']}!")
                        enemy[1] -= dmg
                    else:
                        print(self.l['no_damage'])
                    self.m.sound('atack')
            elif do == '2':
                if self.player["hp"] < self.player["hp_max"]:
                    heal = int(self.player["hp_max"] * 0.2)
                    print(f"{self.l['you_healed']} +{heal} {self.l['hp_restored']}")
                    self.m.sound('heal')
                    self.player["hp"] += heal
                    if self.player["hp"] >= self.player["hp_max"]:
                        self.player["hp"] = self.player["hp_max"]
                else:
                    print(self.l['already_healthy'])
                    continue
            elif do == '3':
                if random.random() < 0.5:
                    print(self.l['escape_success'])
                    break
                else:
                    print(self.l['escape_fail'])
            
            # === CHECK ===
            if enemy[1] <= 0 or self.player["hp"] <= 0:
                break
            
            # === TURN ENEMY ===
            dmg = enemy[3] - self.player["arm"] - random.randint(-1, 1)
            if dmg > 0:
                print(f"{enemy[0]} {self.l['damage_dealt_by']} {dmg} {self.l['damage_to_you']}!")
                self.player["hp"] -= dmg
            else:
                print(f"{enemy[0]} {self.l['enemy_no_damage']}")
            self.m.sound('atack')
            
            # === CHECK ===
            if enemy[1] <= 0 or self.player["hp"] <= 0:
                break
        
        self.m.music(0)
        
        if self.player["hp"] <= 0:
            print(self.l['you_died'])
            input(self.l['press_enter'])
            exit()
        
        print(f"{self.l['you_won']} {enemy[0]}!")
        if enemy[1] <= 0:
            self.gold += enemy[4]
            print(f"{self.l['gained']} +{enemy[4]} {self.l['gold_coins']}")
            self.exp += int(enemy[4] * 2.5)
            print(f"{self.l['gained']} +{int(enemy[4] * 2.5)} {self.l['exp_points']}")
        else:
            self.gold += enemy[4] // 2
            print(f"{self.l['gained']} +{enemy[4] // 2} {self.l['gold_coins']}")
        self.can_upgrade()
    
    def max_exp(self):
        return self.level * 25
    
    def can_upgrade(self):
        if self.exp >= self.max_exp():
            print(self.l['level_up'])
            self.player["hp_max"] += 4
            if self.level % 2 == 0:
                self.player["arm"] += 1
            self.player["dmg"] += 1
            self.exp -= self.max_exp()
            self.level += 1
            self.show_stats()
    
    def rest(self):
        while True:
            anw = self.choice([self.l['rest_hut'], self.l['rest_tent'], self.l['rest_cancel']])
            
            if not anw:
                print(self.l['wrong_choice'])
                continue
            elif anw == '1' and self.gold >= 5:
                self.gold -= 5
                print(self.l['you_rest'])
                self.player['hp'] += 10
                if self.player["hp"] >= self.player["hp_max"]:
                    self.player["hp"] = self.player["hp_max"]
                time.sleep(4)
                self.event = random.choice(['easy', 'normal', 'hard'])
                print(self.l['something_changed'])
                time.sleep(1)
                break
            elif anw == '2' and self.gold >= 10:
                self.gold -= 10
                print(self.l['you_rest'])
                self.player['hp'] += 20
                if self.player["hp"] >= self.player["hp_max"]:
                    self.player["hp"] = self.player["hp_max"]
                time.sleep(4)
                self.event = random.choice(['easy', 'normal', 'hard'])
                print(self.l['something_changed'])
                time.sleep(1)
                break
            elif anw == '3':
                break
            else:
                print(self.l['too_expensive'])

if __name__ == "__main__":
    m = Media()
    m.intro()
    game = Game()
    game.play()
