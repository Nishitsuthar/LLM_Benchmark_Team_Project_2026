from together import Together

client = Together(api_key="tgp_v1_9OcdTuqoXTB0_JRe_0oU778Zy0rtlG2DA3cLuGQl1FU")

response = client.chat.completions.create(
  model="nvidia/nemotron-3-ultra-550b-a55b",
  messages=[
    {
      "role": "user",
      "content": "What are some fun things to do in New York?"
    }
  ]
)
print(response.choices[0].message.content)