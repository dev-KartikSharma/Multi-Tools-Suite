import streamlit as st
from PyPDF2 import PdfMerger
from PIL import Image, ImageEnhance
from streamlit_drawable_canvas import st_canvas
from streamlit_option_menu import option_menu
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="Mini Tool Suite",
    page_icon="🛠️",
    layout="wide"
)

# --- Custom CSS for Sidebar Styling ---
st.markdown("""
<style>
    /* Target the sidebar's inner container */
    [data-testid="stSidebar"] > div:first-child {
        background-color: #ffffff;
        border-radius: 0px 15px 15px 0px;
        box-shadow: 3px 0px 10px rgba(0,0,0,0.1);
        padding-top: 2rem; /* Add some space at the top */
    }
</style>
""", unsafe_allow_html=True)


# --- Sidebar for Navigation ---
with st.sidebar:
    tool_choice = option_menu(
        menu_title="",
        options=["Home", "PDF Merger", "PDF Compressor", "Photo Enhancer", "Drawing Canvas"],
        icons=["house-fill", "file-earmark-zip-fill", "file-earmark-break-fill", "image-fill", "palette2"],
        menu_icon=None,
        default_index=0,
        styles={
            "container": {
                "padding": "2", 
                "background-color": "#FFFFFF",
            },
            "icon": {"color": "black", "font-size": "25px"}, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin":"5px", 
                "--hover-color": "#eee",
                "border-radius": "5px",
            },
            "nav-link-selected": {"background-color": "#808080"},
        }
    )

# --- Home Page ---
def home_page():
    st.markdown("<h1 style='text-align: center;'>Mini Tool Suite 🛠️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Your one-stop shop for simple document and image tasks.</p>", unsafe_allow_html=True)
    st.divider()

    st.subheader("About This App")
    st.write("""
    This application provides a collection of simple, yet powerful tools to help you with common file manipulation tasks.
    All features are completely free to use. Navigate using the sidebar on the left to select a tool and get started.
    """)
    st.divider()

    st.subheader("Built By")
    st.markdown("""
    - **Me** (Kartik Sharma)
    - **Contact:** kartiksharma17012007@gmail.com
    - **GitHub:** [Kartik Sharma](https://github.com/dev-KartikSharma)
    """)
    st.info("👈 Select a tool from the sidebar to begin!")


# --- 1. PDF Merger ---
def pdf_merger_tool():
    st.header("PDF Merger")
    st.markdown("Upload multiple PDF files and merge them into a single document. The files will be merged in the order they are listed.")

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
        help="Upload the PDFs you want to merge."
    )

    if uploaded_files:
        st.write(f"You have uploaded {len(uploaded_files)} PDF files.")

        if st.button("Merge PDFs", type="primary"):
            merger = PdfMerger()
            try:
                for pdf_file in uploaded_files:
                    pdf_file.seek(0)
                    merger.append(pdf_file)

                pdf_buffer = io.BytesIO()
                merger.write(pdf_buffer)
                merger.close()
                pdf_buffer.seek(0)

                st.success("PDFs merged successfully!")
                st.download_button(
                    label="⬇️ Download Merged PDF",
                    data=pdf_buffer,
                    file_name="merged_document.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- 2. PDF Compressor ---
def pdf_compressor_tool():
    st.header("PDF Compressor")
    st.markdown("Upload a PDF file to reduce its size. Note: Compression effectiveness varies.")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload the PDF you want to compress."
    )

    if uploaded_file:
        original_size = len(uploaded_file.getvalue())
        st.info(f"Original file size: {original_size / 1_000_000:.2f} MB")

        if st.button("Compress PDF", type="primary"):
            try:
                from PyPDF2 import PdfReader, PdfWriter
                
                reader = PdfReader(uploaded_file)
                writer = PdfWriter()

                for page in reader.pages:
                    writer.add_page(page)

                for page in writer.pages:
                    page.compress_content_streams()

                pdf_buffer = io.BytesIO()
                writer.write(pdf_buffer)
                pdf_buffer.seek(0)
                
                compressed_size = len(pdf_buffer.getvalue())
                reduction = (original_size - compressed_size) / original_size * 100

                st.success("PDF compressed successfully!")
                st.write(f"New file size: {compressed_size / 1_000_000:.2f} MB")
                st.write(f"Size reduction: {reduction:.2f}%")

                st.download_button(
                    label="⬇️ Download Compressed PDF",
                    data=pdf_buffer,
                    file_name="compressed_document.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"An error occurred during compression: {e}")


# --- 3. Photo Enhancer ---
def photo_enhancer_tool():
    st.header("Photo Enhancer")
    st.markdown("Upload an image and apply simple enhancements using the controls in the sidebar.")

    uploaded_image = st.file_uploader(
        "Choose an image",
        type=["png", "jpg", "jpeg"],
        help="Upload the image you want to enhance."
    )

    # Enhancement controls are moved to the sidebar within the tool function
    st.sidebar.subheader("Enhancement Controls")
    brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)
    sharpness = st.sidebar.slider("Sharpness", 0.5, 3.0, 1.0)

    if uploaded_image:
        img = Image.open(uploaded_image)
        
        enhancer_brightness = ImageEnhance.Brightness(img)
        enhanced_img = enhancer_brightness.enhance(brightness)
        
        enhancer_contrast = ImageEnhance.Contrast(enhanced_img)
        enhanced_img = enhancer_contrast.enhance(contrast)

        enhancer_sharpness = ImageEnhance.Sharpness(enhanced_img)
        enhanced_img = enhancer_sharpness.enhance(sharpness)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Image")
            st.image(img, use_column_width=True, caption="Original")
        with col2:
            st.subheader("Enhanced Image")
            st.image(enhanced_img, use_column_width=True, caption="Enhanced")
            
        img_buffer = io.BytesIO()
        enhanced_img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        st.download_button(
            label="⬇️ Download Enhanced Image",
            data=img_buffer,
            file_name="enhanced_image.png",
            mime="image/png"
        )


# --- 4. Drawing Canvas ---
def drawing_canvas_tool():
    st.header("Drawing Canvas")
    st.markdown("Unleash your creativity! Use the controls in the sidebar to change your brush and colors.")

    # Canvas controls are moved to the sidebar within the tool function
    st.sidebar.subheader("Canvas Controls")
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color: ", "#000000")
    bg_color = st.sidebar.color_picker("Background color: ", "#EEEEEE")
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:", ("freedraw", "line", "rect", "circle", "transform")
    )
    
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=400,
        width=600,
        drawing_mode=drawing_mode,
        key="canvas",
    )

    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data)
        try:
            img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            st.download_button(
                label="⬇️ Download Drawing",
                data=img_buffer,
                file_name="drawing.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"Could not process image for download: {e}")


# --- Main App Logic ---
if tool_choice == "Home":
    home_page()
elif tool_choice == "PDF Merger":
    pdf_merger_tool()
elif tool_choice == "PDF Compressor":
    pdf_compressor_tool()
elif tool_choice == "Photo Enhancer":
    photo_enhancer_tool()
elif tool_choice == "Drawing Canvas":
    drawing_canvas_tool()
