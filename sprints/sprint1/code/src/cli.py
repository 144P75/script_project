class CLIHandler:
    """Presentation Layer: จัดการการแสดงผล UI และ Input Validation"""

    @staticmethod
    def display_welcome():
        print("=" * 50)
        print("     VIRTUAL PET SIMULATOR (AI Companion)     ")
        print("=" * 50)

    @staticmethod
    def display_status(pet):
        pet.apply_time_decay()
        print(f"\n--- สถานะของ {pet.name} [{pet.mood_tracker.get_mood()}] ---")
        print(f"  ความหิว (Hunger)   : [{pet.mood_tracker.hunger}/100]")
        print(f"  พลังงาน (Energy)   : [{pet.mood_tracker.energy}/100]")
        print(f"  ความสุข (Happiness): [{pet.mood_tracker.happiness}/100]")
        print("-" * 40)

    @staticmethod
    def get_command_input() -> str:
        """รับค่า ทำความสะอาดอินพุตด้วย .strip().lower()"""
        try:
            raw_input = input("เลือกคำสั่ง [feed / play / sleep / fact / save / quit]: ")
            return raw_input.strip().lower()
        except (KeyboardInterrupt, EOFError):
            return "quit"