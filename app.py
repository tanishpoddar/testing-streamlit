import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="SpeedScope", layout="wide")

def create_speed_test():
    return """
    <div id="speed-test">
        <script>
        class SpeedTest {
            async measureLatency() {
                const start = performance.now();
                await fetch('https://www.google.com/favicon.ico');
                return performance.now() - start;
            }

            async downloadTest() {
                const fileSize = 5242880; // 5MB
                const startTime = performance.now();
                const response = await fetch('https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css');
                const reader = response.body.getReader();
                let receivedLength = 0;

                while(true) {
                    const {done, value} = await reader.read();
                    if (done) break;
                    receivedLength += value.length;
                }

                const duration = (performance.now() - startTime) / 1000;
                return (receivedLength * 8 / duration) / 1000000; // Mbps
            }

            async uploadTest() {
                const size = 2000000; // 2MB
                const data = new Blob([new ArrayBuffer(size)]);
                const startTime = performance.now();
                
                await fetch('https://httpbin.org/post', {
                    method: 'POST',
                    body: data
                });

                const duration = (performance.now() - startTime) / 1000;
                return (size * 8 / duration) / 1000000; // Mbps
            }

            async runTest() {
                try {
                    const ping = await this.measureLatency();
                    const download = await this.downloadTest();
                    const upload = await this.uploadTest();
                    
                    window.parent.Streamlit.setComponentValue({
                        ping: Math.round(ping),
                        download: download.toFixed(1),
                        upload: upload.toFixed(1)
                    });
                } catch (error) {
                    console.error('Test failed:', error);
                }
            }
        }

        new SpeedTest().runTest();
        </script>
    </div>
    """

def format_speed(speed):
    try:
        speed = float(speed)
        return f"{speed:.1f}"
    except:
        return "0.0"

if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_results' not in st.session_state:
    st.session_state.current_results = {"download": "0.0", "upload": "0.0", "ping": "0"}

col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image("🚀", width=50)
with col_title:
    st.title("SpeedScope")
    st.caption("Your Internet Speed Analyzer")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Download Speed", f"{format_speed(st.session_state.current_results['download'])} Mbps")

with col2:
    st.metric("Upload Speed", f"{format_speed(st.session_state.current_results['upload'])} Mbps")

with col3:
    st.metric("Ping", f"{st.session_state.current_results['ping']} ms")

if st.button("Start Speed Test", type="primary"):
    with st.spinner("Testing your connection..."):
        components.html(create_speed_test(), height=0)

if st.session_state.history:
    st.subheader("Speed History")
    fig = go.Figure()
    
    times = [h["timestamp"] for h in st.session_state.history]
    downloads = [float(h["download"]) for h in st.session_state.history]
    uploads = [float(h["upload"]) for h in st.session_state.history]
    
    fig.add_trace(go.Scatter(x=times, y=downloads, name="Download", line=dict(color="#00b4d8")))
    fig.add_trace(go.Scatter(x=times, y=uploads, name="Upload", line=dict(color="#90e0ef")))
    
    fig.update_layout(
        plot_bgcolor="#1a1f25",
        paper_bgcolor="#1a1f25",
        font_color="white",
        xaxis=dict(title="Time"),
        yaxis=dict(title="Speed (Mbps)")
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Made with ❤️ by Tanish Poddar")