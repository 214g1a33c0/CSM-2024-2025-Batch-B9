# import difflib

# phrase_to_gif = {
#     "any questions": "isl_translator/ISL_Gifs/any questions.gif",
#     "i am fine": "isl_translator/ISL_Gifs/i am fine.gif",  # Updated mapping for "i am fine"
#     "hello": "isl_translator/ISL_Gifs/hello.gif",
#     "thank you": "isl_translator/ISL_Gifs/thank_you.gif",
#     "goodbye": "isl_translator/ISL_Gifs/goodbye.gif",
#     "are you angry": "isl_translator/ISL_Gifs/are you angry.gif",
#     "are you busy": "isl_translator/ISL_Gifs/are you busy.gif",
#     "are you hungry": "isl_translator/ISL_Gifs/are you hungry.gif",
#     "i am tired": "isl_translator/ISL_Gifs/i am tired.gif",
#     "i love to shop": "isl_translator/ISL_Gifs/i love to shop.gif",
#     "what is your name": "isl_translator/ISL_Gifs/what is your name.gif",
#     "where is the bathroom": "isl_translator/ISL_Gifs/where is the bathroom.gif",
#     "can we meet tomorrow": "isl_translator/ISL_Gifs/can we meet tomorrow.gif",
#     "did you finish homework": "isl_translator/ISL_Gifs/did you finish homework.gif",
#     "please wait for sometime": "isl_translator/ISL_Gifs/please wait for sometime.gif",



#     "Hello": "isl_translator/ISL_Gifs/hello.gif",
#     "Thank you": "isl_translator/ISL_Gifs/thank_you.gif",
#     "Goodbye": "isl_translator/ISL_Gifs/goodbye.gif",
#     "Are you angry": "isl_translator/ISL_Gifs/are you angry.gif",
#     "Are you busy": "isl_translator/ISL_Gifs/are you busy.gif",
#     "Are you hungry": "isl_translator/ISL_Gifs/are you hungry.gif",
#     "I am tired": "isl_translator/ISL_Gifs/i am tired.gif",
#     "I love to shop": "isl_translator/ISL_Gifs/i love to shop.gif",
#     "What is your name": "isl_translator/ISL_Gifs/what is your name.gif",
#     # "How are you": "isl_translator/ISL_Gifs/how are you.gif",  # Added mapping for "How are you"


#     "Where is the bathroom": "isl_translator/ISL_Gifs/where is the bathroom.gif",
#     "Can we meet tomorrow": "isl_translator/ISL_Gifs/can we meet tomorrow.gif",
#     "Did you finish homework": "isl_translator/ISL_Gifs/did you finish homework.gif",
#     "Please wait for sometime": "isl_translator/ISL_Gifs/please wait for sometime.gif",
#     "hi": "isl_translator/ISL_Gifs/hello.gif",
#     "thank you": "isl_translator/ISL_Gifs/thank_you.gif",  # Added mapping for "thank you"


#     "what are you doing":"isl_translator/ISL_Gifs/what are you doing.gif" # Added mapping for "hi"

#     # Add more phrases as needed
# }

# letter_to_image = {
#     'a': "isl_translator/letters/a.jpg",
#     'b': "isl_translator/letters/b.jpg",
#     'c': "isl_translator/letters/c.jpg",
#     'd': "isl_translator/letters/d.jpg",
#     'e': "isl_translator/letters/e.jpg",
#     'f': "isl_translator/letters/f.jpg",
#     'g': "isl_translator/letters/g.jpg",
#     'h': "isl_translator/letters/h.jpg",
#     'i': "isl_translator/letters/i.jpg",
#     'j': "isl_translator/letters/j.jpg",
#     'k': "isl_translator/letters/k.jpg",
#     'l': "isl_translator/letters/l.jpg",
#     'm': "isl_translator/letters/m.jpg",
#     'n': "isl_translator/letters/n.jpg",
#     'o': "isl_translator/letters/o.jpg",
#     'p': "isl_translator/letters/p.jpg",
#     'q': "isl_translator/letters/q.jpg",
#     'r': "isl_translator/letters/r.jpg",
#     's': "isl_translator/letters/s.jpg",
#     't': "isl_translator/letters/t.jpg",
#     'u': "isl_translator/letters/u.jpg",
#     'v': "isl_translator/letters/v.jpg",
#     'w': "isl_translator/letters/w.jpg",
#     'x': "isl_translator/letters/x.jpg",
#     'y': "isl_translator/letters/y.jpg",
#     'z': "isl_translator/letters/z.jpg",
#     ' ': "isl_translator/letters/space.png", 


# }

# def translate_text_to_sign(text):
#     # Split the input text into phrases
#     phrases = [phrase.strip() for phrase in text.lower().split(", ")]

#     output_paths = []
#     similarity_cutoff = 0.7  # Adjust this threshold as needed

#     for phrase in phrases:
#         # Check if the exact phrase exists in the mapping
#         if phrase in phrase_to_gif:
#             output_paths.append(phrase_to_gif[phrase])
#             continue

#         # Check for similar phrases if exact match not found
#         similar_phrases = difflib.get_close_matches(
#             phrase, 
#             phrase_to_gif.keys(), 
#             n=1, 
#             cutoff=similarity_cutoff
#         )
#         if similar_phrases:
#             output_paths.append(phrase_to_gif[similar_phrases[0]])
#             continue

#         # If no similar phrase found, break down into letters
#         for char in phrase:
#             if char.lower() in letter_to_image:
#                 output_paths.append(letter_to_image[char.lower()])
#             else:
#                 print(f"Warning: No mapping found for character '{char}'")

#     return output_paths

# if __name__ == "__main__":
#     input_text = "How are you, I am good"
#     output = translate_text_to_sign(input_text)
#     print(output)  # This will print the list of paths to GIFs and images




from sentence_transformers import SentenceTransformer, util
import numpy as np
import tensorflow as tf


# Pre-trained model for sentence embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

phrase_to_gif = {
    # Original phrase mappings (lowercase keys only)
    "any questions": "isl_translator/ISL_Gifs/any questions.gif",
    "i am fine": "isl_translator/ISL_Gifs/i am fine.gif",
    "hello": "isl_translator/ISL_Gifs/hello.gif",
    "thank you": "isl_translator/ISL_Gifs/thank_you.gif",
    "goodbye": "isl_translator/ISL_Gifs/goodbye.gif",
    "are you angry": "isl_translator/ISL_Gifs/are you angry.gif",
    "what are you doing": "isl_translator/ISL_Gifs/what are you doing.gif"
    # Add other phrases...
}

# Generate embeddings for known phrases
phrase_list = list(phrase_to_gif.keys())
phrase_embeddings = model.encode(phrase_list, convert_to_tensor=True)

letter_to_image = {
    # Existing letter mappings...
    'a': "isl_translator/letters/a.jpg",
    'b': "isl_translator/letters/b.jpg",
    'c': "isl_translator/letters/c.jpg",
    'd': "isl_translator/letters/d.jpg",
    'e': "isl_translator/letters/e.jpg",
    'f': "isl_translator/letters/f.jpg",
    'g': "isl_translator/letters/g.jpg",
    'h': "isl_translator/letters/h.jpg",
    'i': "isl_translator/letters/i.jpg",
    'j': "isl_translator/letters/j.jpg",
    'k': "isl_translator/letters/k.jpg",
    'l': "isl_translator/letters/l.jpg",
    'm': "isl_translator/letters/m.jpg",
    'n': "isl_translator/letters/n.jpg",
    'o': "isl_translator/letters/o.jpg",
    'p': "isl_translator/letters/p.jpg",
    'q': "isl_translator/letters/q.jpg",
    'r': "isl_translator/letters/r.jpg",
    's': "isl_translator/letters/s.jpg",
    't': "isl_translator/letters/t.jpg",
    'u': "isl_translator/letters/u.jpg",
    'v': "isl_translator/letters/v.jpg",
    'w': "isl_translator/letters/w.jpg",
    'x': "isl_translator/letters/x.jpg",
    'y': "isl_translator/letters/y.jpg",
    'z': "isl_translator/letters/z.jpg",
    ' ': "isl_translator/letters/space.png", 
}

def translate_text_to_sign(text, similarity_threshold=0.72):
    """Convert input text to sign language resources using deep learning."""
    phrases = [phrase.strip().lower() for phrase in text.split(", ")]
    output_paths = []

    for phrase in phrases:
        # Direct match check
        if phrase in phrase_to_gif:
            output_paths.append(phrase_to_gif[phrase])
            continue

        # Semantic similarity search
        query_embedding = model.encode(phrase, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, phrase_embeddings)[0]
        max_score_idx = np.argmax(cos_scores)
        max_score = cos_scores[max_score_idx].item()

        if max_score >= similarity_threshold:
            matched_phrase = phrase_list[max_score_idx]
            output_paths.append(phrase_to_gif[matched_phrase])
        else:
            # Character-level fallback
            for char in phrase:
                if char in letter_to_image:
                    output_paths.append(letter_to_image[char])
                else:
                    print(f"Unsupported character: {char}")

    return output_paths