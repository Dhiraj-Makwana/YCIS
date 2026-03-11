from transformers import pipeline

toxicity_pipeline = pipeline(
    "text-classification",
    model="unitary/toxic-bert"
)


def detect_toxicity(comments, batch_size=16):

    toxic_count = 0
    clean_count = 0

    for i in range(0, len(comments), batch_size):

        batch = comments[i:i + batch_size]
        results = toxicity_pipeline(batch)

        for result in results:

            label = result["label"].lower()

            if "toxic" in label:
                toxic_count += 1
            else:
                clean_count += 1

    return {
        "toxic": toxic_count,
        "clean": clean_count
    }