# import asyncio
# import os
# from dotenv import load_dotenv
# from fastmcp import Client
# from google import genai
# from google.genai import types
# from google.genai.types import Tool, FunctionDeclaration

# load_dotenv()

# mcp_client = Client("server1.py")
# gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# def clean_schema(schema):
#     """
#     Recursively cleans JSON schema for Gemini compatibility:
#     - Removes 'title'
#     - Removes 'additionalProperties'
#     - Processes nested dicts and lists
#     """
#     if isinstance(schema, dict):
#         # Drop invalid keys
#         schema.pop("title", None)
#         schema.pop("additionalProperties", None)

#         # Recurse into children
#         return {k: clean_schema(v) for k, v in schema.items()}
#     elif isinstance(schema, list):
#         return [clean_schema(item) for item in schema]
#     else:
#         return schema


# def convert_mcp_tools_to_gemini(mcp_tools):
#     gemini_tools = []
#     for tool in mcp_tools:
#         parameters = clean_schema(tool.inputSchema)

#         fd = FunctionDeclaration(
#             name=tool.name,
#             description=tool.description,
#             parameters=parameters
#         )
#         gemini_tools.append(Tool(function_declarations=[fd]))
#     return gemini_tools


import streamlit as st
import pandas as pd
import asyncio
import os
from dotenv import load_dotenv
from fastmcp import Client
from google import genai
from google.genai import types
from viz_tools import generate_visualization
from mcp_utils import convert_mcp_tools_to_gemini

load_dotenv()

# Initialize clients
mcp_client = Client("server1.py")
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("📊 MCP EDA & Dashboard Generator")

uploaded_file = st.file_uploader("Upload a CSV dataset", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Preview of Dataset", df.head())

    async def run_analysis(user_query: str):
        async with mcp_client:
            mcp_tools = await mcp_client.session.list_tools()
            gemini_tools = convert_mcp_tools_to_gemini(mcp_tools.tools)

            config = types.GenerateContentConfig(
                temperature=0,
                tools=gemini_tools,
            )

            # Send schema + user query to Gemini
            contents = f"""
            Dataset schema:
            {df.dtypes.to_dict()}

            User request:
            {user_query}
            """
            response = await gemini_client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=config,
            )

            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.function_call:
                        fn = part.function_call.name
                        args = part.function_call.args
                        st.info(f"Gemini is calling `{fn}` with {args}")

                        tool_result = await mcp_client.session.call_tool(fn, args)

                        followup = await gemini_client.aio.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[
                                f"Schema: {df.dtypes.to_dict()}",
                                response.candidates[0].content,
                                types.Part.from_function_response(
                                    name=fn,
                                    response={"result": tool_result},
                                ),
                            ],
                            config=config,
                        )
                        return followup.text
            return response.text

    user_query = st.text_input("Ask Gemini to generate a visualization (e.g. 'Show histogram of age')")
    if user_query:
        explanation = asyncio.run(run_analysis(user_query))
        st.success("Gemini Explanation:")
        st.write(explanation)

        # For demo: manual chart render (Gemini could suggest params here too)
        chart_type = st.selectbox("Chart type", ["hist", "scatter", "bar", "heatmap"])
        x_col = st.selectbox("X-axis", df.columns)
        y_col = st.selectbox("Y-axis (optional)", ["None"] + list(df.columns))

        if st.button("Generate Chart"):
            img_b64 = generate_visualization(df, chart_type, x_col, None if y_col == "None" else y_col)
            st.image(f"data:image/png;base64,{img_b64}")
