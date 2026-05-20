"""
components/sidebar.py
=====================
Sidebar UI — file uploader, dataset info, action buttons.
No custom CSS overrides here — all styling is in assets/style.css.
"""

import streamlit as st


def render_sidebar() -> object | None:
    """Render sidebar. Returns UploadedFile or None."""

    with st.sidebar:

        # ── Logo ──
        st.markdown(
            """
            <div style="padding:1rem 0 1.25rem;">
              <div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:800;
                          background:linear-gradient(135deg,#f0f0f8,#6366f1);
                          -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                          background-clip:text;">
                📊 AI BI Dashboard
              </div>
              <div style="font-size:0.73rem; color:#55556a; margin-top:0.2rem;">
                Powered by Gemini 1.5 Flash
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Upload section ──
        st.markdown(
            "**📁 Upload Your Data**",
        )

        uploaded_file = st.file_uploader(
            label="Drop a CSV or Excel file here",
            type=["csv", "xlsx", "xls"],
            help="Supported: .csv, .xlsx, .xls — max 200 MB",
        )

        st.caption("✓ CSV · ✓ Excel (.xlsx / .xls) · Max 200 MB")

        st.divider()

        # ── Tip ──
        st.info(
            "💡 **Sidebar closed?**  \nClick the **›** arrow at the top-left of the screen to reopen.",
            icon=None,
        )

        st.divider()

        # ── Dataset info after upload ──
        result = st.session_state.get("clean_result")
        if result is not None:
            df = result.df
            st.markdown("**📋 Dataset Info**")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Rows",    f"{df.shape[0]:,}")
                st.metric("Numeric", str(len(df.select_dtypes(include=["number"]).columns)))
                st.metric("Health",  f"{result.health_score}/100")
            with col2:
                st.metric("Columns", str(df.shape[1]))
                st.metric("Dates",   str(len(df.select_dtypes(include=["datetime64"]).columns)))
                st.metric("Dupes ✂", str(result.duplicates_removed))

            st.divider()

            if st.button("🔄 Regenerate AI Charts", use_container_width=True, type="primary"):
                for key in ["chart_configs", "anomaly_narratives"]:
                    st.session_state.pop(key, None)
                st.rerun()

            if st.button("🗑️ Upload New File", use_container_width=True):
                for key in [
                    "clean_result", "gemini_summary", "messages",
                    "chart_configs", "anomaly_narratives", "file_name",
                ]:
                    st.session_state.pop(key, None)
                st.rerun()

        # ── Footer ──
        st.markdown(
            """
            <div style="padding:2rem 0 0.5rem; font-size:0.7rem; color:#55556a; line-height:1.7;">
              Streamlit · Pandas · Plotly · Gemini<br>₹0 / month · 100% free
            </div>
            """,
            unsafe_allow_html=True,
        )

    return uploaded_file
