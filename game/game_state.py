class GameState:
    def __init__(self):
        self.current_state = "menu"  # menu, playing, win, lose
        self.current_phase = 1
        self.loop_count = 0  # Counter for how many times player has beaten all phases
    
    def change_state(self, new_state):
        self.current_state = new_state
    
    def start_game(self):
        self.current_state = "playing"
        self.current_phase = 1
        self.loop_count = 0
    
    def advance_phase(self):
        self.current_phase += 1
        
        # If we've completed all phases, reset to phase 1 with all gimmicks active
        if self.current_phase > 4:
            self.current_phase = 1
            self.loop_count += 1
    
    def get_active_gimmicks(self):
        """Returns a dictionary of which gimmicks are active based on current phase and loop count"""
        gimmicks = {
            "basic_projectiles": True,  # Always active
            "stomp_attack": self.current_phase >= 2 or self.loop_count > 0,
            "lava_rising": self.current_phase >= 3 or self.loop_count > 0,
            "lava_worms": self.current_phase >= 3 or self.loop_count > 0,
            "invert_lava": self.current_phase == 4 or self.loop_count > 0,
            "blinding_rocks": self.current_phase >= 4 or self.loop_count > 0
        }
        return gimmicks
