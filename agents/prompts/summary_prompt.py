summary_prompt = """
Studio Ghibli style illustration. The animal is the main focus, depicted from its perspective, looking towards its owner. The animal's current condition and the surrounding environment are clearly visible and evocative. In the center of the image, a thought bubble or text overlay displays the animal's message to its owner in a whimsical, hand-drawn font.

Examples of text to include in the image:

"{PET NAME} : Hurry up, I'm starving! Feed me now, pleeeese!"

"{PET NAME} : The weather is perfect! Leash time! Let's go to a walk!"

"{PET NAME} : Oh, a butterfly! Can we chase it, can we?!"

"{PET NAME} : Another nap? But you just woke up! Play with me!"

"{PET NAME} : My favorite blanket... it smells like you. Zzz..."

Please tell me:

What animal should be depicted? (e.g., a fluffy cat, a playful dog, a curious rabbit)

What is the animal's current condition and what is the surrounding situation? (e.g., a hungry cat by an empty bowl, a dog excitedly waiting by the door, a rabbit napping peacefully on a sunny windowsill)

What message should the animal be conveying to its owner? (Choose one of the examples above, or create a new one!)

Let's assume the PET NAME is COCO and reflect this on text message.
"""
