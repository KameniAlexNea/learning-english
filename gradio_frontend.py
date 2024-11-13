import gradio as gr

from learning_language.backend import (
    evaluate,
    prepare,
    suggest_llm_answer,
    suggest_topic,
)


# Function to generate a new topic
def generate_new_topic():
    response = suggest_topic()
    if "Error" in response["topic"]:
        return None, response["topic"]
    else:
        return response["topic"], ""


# Function to evaluate the user's response
def evaluate_response(user_input, current_topic):
    if not user_input.strip():
        return "Please provide a response."

    user_data = prepare({"user_input": user_input, "topic": current_topic})
    evaluation = evaluate(user_data)
    if "Error" in evaluation["evaluation"]:
        return evaluation["evaluation"]
    else:
        return evaluation["evaluation"]


# Function to suggest an answer
def suggest_answer(current_topic):
    user_data = prepare({"user_input": "", "topic": current_topic})
    suggested_answer = suggest_llm_answer(user_data)
    if "Error" in suggested_answer["suggested_answer"]:
        return suggested_answer["suggested_answer"]
    else:
        return suggested_answer["suggested_answer"]


# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Writing Assistant")

    with gr.Row():
        generate_button = gr.Button("Generate New Topic")
        topic_display = gr.Textbox(label="Current Topic", interactive=False)
        error_message = gr.Textbox(
            label="Error Message", interactive=False, visible=False
        )

    with gr.Row():
        user_input = gr.Textbox(label="Write your response here:", lines=5)

    with gr.Row():
        evaluate_button = gr.Button("Evaluate Response")
        suggest_button = gr.Button("Suggest an Answer")

    with gr.Row():
        evaluation_display = gr.Textbox(label="Evaluation", interactive=False)
        suggestion_display = gr.Textbox(label="Suggested Answer", interactive=False)

    # Event handlers
    generate_button.click(
        fn=generate_new_topic, inputs=None, outputs=[topic_display, error_message]
    )

    evaluate_button.click(
        fn=evaluate_response,
        inputs=[user_input, topic_display],
        outputs=[evaluation_display],
    )

    suggest_button.click(
        fn=suggest_answer, inputs=[topic_display], outputs=[suggestion_display]
    )

# Launch the Gradio interface
demo.launch()
