import pandas as pd
from integrations.monday_api import MondayClient
from processing import data_cleaner, metrics_engine
from agent.query_interpreter import QueryInterpreter
from agent.insight_generator import InsightGenerator
from agent.dynamic_engine import DynamicEngine
from config import settings

class BIAgent:
    def __init__(self):
        self.monday = MondayClient()
        self.interpreter = QueryInterpreter()
        self.generator = InsightGenerator()
        self.dynamic_engine = DynamicEngine()
        
    def _fetch_all_data(self):
        """Fetch and clean data from live Monday.com boards with Local CSV Fallback."""
        data_source_label = "Deals Board / Work Orders Board"
        try:
            deals_df = self.monday.get_deals_board_data()
            work_orders_df = self.monday.get_work_orders_board_data()
            if deals_df.empty or work_orders_df.empty:
                raise ValueError("API returned empty DataFrames.")
        except Exception as e:
            print(f"Monday API Error, falling back to local CSV: {e}")
            try:
                # Local CSV Fallback
                deals_df = pd.read_csv("d:/Skylark/data/Deal_funnel_Data.csv")
                work_orders_df = pd.read_csv("d:/Skylark/data/Work_Order_Tracker_Data.csv")
                data_source_label = "Local CSV Files (Fallback)"
                
                # The CSV headers need to roughly match what data_cleaner expects.
                # Since we synced the API columns to the CSV headers earlier, 
                # the CSV headers should mostly work out of the box with data_cleaner.
            except Exception as csv_err:
                print(f"Local CSV Fallback failed: {csv_err}")
                deals_df = pd.DataFrame()
                work_orders_df = pd.DataFrame()
                data_source_label = "Error: No Data Available"

        # Cleaning
        deals_df = data_cleaner.clean_deals_data(deals_df)
        work_orders_df = data_cleaner.clean_work_orders_data(work_orders_df)

        return deals_df, work_orders_df, data_source_label

    def process_query(self, user_query):
        """Main orchestrator flow with enhanced validation and traceability."""
        # 1. Interpret Query
        intent = self.interpreter.interpret(user_query)
        
        # 2. Get Data
        deals_df, wo_df, data_source_label = self._fetch_all_data()
        
        metric_type = intent.get('metric')
        sector = intent.get('sector', 'all')
        
        # Determine strict board source based on metric type to prevent LLM hallucinations
        deals_metrics = ['pipeline_value', 'top_clients', 'top_deals']
        wo_metrics = ['revenue_by_sector', 'delayed_projects', 'work_order_completion_rate', 'active_work_orders', 'work_order_status_breakdown']
        
        if metric_type in deals_metrics:
            source = 'deals'
        elif metric_type in wo_metrics:
            source = 'work_orders'
        elif metric_type == 'custom':
            source = 'both'
        else:
            source = 'deals'
            
        active_df = deals_df if source == 'deals' else wo_df
        
        if "Fallback" in data_source_label or "Error" in data_source_label:
            board_name = data_source_label
        else:
            if source == 'deals':
                board_name = "Deals Board"
            elif source == 'work_orders':
                board_name = "Work Orders Board"
            else:
                board_name = "Dynamic Multi-Board Analysis"
        
        # Define strictly required columns to answer the question
        strict_req_cols = []
        if metric_type == 'pipeline_value':
            strict_req_cols = ['Masked Deal value']
        elif metric_type in ['top_clients', 'top_deals']:
            strict_req_cols = ['Unified_Client_Code', 'Deal Name', 'Unified_Sector', 'Masked Deal value']
        elif metric_type == 'revenue_by_sector':
            strict_req_cols = ['Unified_Sector', 'Amount in Rupees (Excl of GST) (Masked)']
        elif metric_type == 'delayed_projects':
            strict_req_cols = ['Execution Status', 'Data Delivery Date']
        elif metric_type == 'work_order_completion_rate':
            strict_req_cols = ['Execution Status']
        elif metric_type == 'active_work_orders':
            strict_req_cols = ['Execution Status']
        elif metric_type == 'work_order_status_breakdown':
            strict_req_cols = ['Execution Status']
            
        if sector != 'all':
            strict_req_cols.append('Unified_Sector')
                
        # 3. Dynamic Column Fallback Check
        missing_cols = [col for col in strict_req_cols if col not in active_df.columns]
        if missing_cols and board_name in ["Deals Board", "Work Orders Board"]:
            print(f"Dynamic Fallback Triggered: Missing columns {missing_cols} in {board_name}")
            try:
                if source == 'deals':
                    active_df = pd.read_csv("d:/Skylark/data/Deal_funnel_Data.csv")
                    active_df = data_cleaner.clean_deals_data(active_df)
                else:
                    active_df = pd.read_csv("d:/Skylark/data/Work_Order_Tracker_Data.csv")
                    active_df = data_cleaner.clean_work_orders_data(active_df)
                board_name = "Local CSV Files (Dynamic Column Fallback)"
            except Exception as e:
                print(f"Dynamic Fallback failed: {e}")
        
        # 4. Data Validation Step (Anti-Hallucination)
        validation_errors = []
        if active_df.empty:
            return {
                "error": "Unable to retrieve data from monday.com board. The result cannot be generated.",
                "traceability": {
                    "board": board_name,
                    "records": 0,
                    "columns": []
                }
            }

        # 5. Calculate Specific Metrics
        result_metric = None
        
        # Filter by sector if applicable
        if sector != 'all' and 'Unified_Sector' in active_df.columns:
            active_df = active_df[active_df['Unified_Sector'].str.lower() == sector.lower()]

        if metric_type == 'pipeline_value':
            val = metrics_engine.total_pipeline_value(active_df)
            result_metric = f"Total Pipeline Value: ₹{val:,.2f}"
            req_cols = ['Masked Deal value']
        elif metric_type in ['top_clients', 'top_deals']:
            top = metrics_engine.top_clients_with_largest_deals(active_df)
            cols_to_use = [c for c in strict_req_cols if c in top.columns]
            result_metric = top[cols_to_use].to_dict(orient='records')
            req_cols = cols_to_use
        elif metric_type == 'revenue_by_sector':
            rev = metrics_engine.revenue_by_sector(active_df)
            result_metric = rev.to_dict()
            req_cols = ['Unified_Sector', 'Amount in Rupees (Excl of GST) (Masked)']
        elif metric_type == 'delayed_projects':
            delayed = metrics_engine.delayed_projects(active_df)
            result_metric = delayed.to_dict(orient='records') if not delayed.empty else "No delayed projects found."
            req_cols = ['Execution Status', 'Data Delivery Date']
        elif metric_type == 'work_order_completion_rate':
            rate = metrics_engine.work_order_completion_rate(active_df)
            result_metric = f"{rate:.1f}%"
            req_cols = ['Execution Status']
        elif metric_type == 'active_work_orders':
            val = metrics_engine.active_work_orders(active_df)
            result_metric = f"Active Work Orders: {int(val)}"
            req_cols = ['Execution Status']
        elif metric_type == 'work_order_status_breakdown':
            breakdown = metrics_engine.work_order_status_breakdown(active_df)
            result_metric = breakdown.to_dict()
            req_cols = ['Execution Status']
        elif metric_type == 'custom':
            result_metric = self.dynamic_engine.generate_and_execute(user_query, deals_df, wo_df)
            req_cols = []
        else:
            result_metric = "Unsupported metric type."
            req_cols = []

        # 5. Traceability Metadata
        traceability = {
            "board": board_name,
            "records": len(active_df),
            "columns": [c for c in req_cols if c in active_df.columns]
        }

        # 6. Generate Insight (using new reporting standards prompt)
        insight = self.generator.generate_executive_report(user_query, traceability, result_metric)
        
        return {
            "status": "success",
            "intent": intent,
            "metric_data": result_metric,
            "traceability": traceability,
            "report": insight
        }

    def get_weekly_summary(self):
        """Generate high level dashboard summary."""
        deals_df, wo_df, data_source_label = self._fetch_all_data()
        
        total_val = metrics_engine.total_pipeline_value(deals_df)
        rev_dist = metrics_engine.revenue_by_sector(wo_df)
        top_sector = rev_dist.index[0] if not rev_dist.empty else "N/A"
        delayed = len(metrics_engine.delayed_projects(wo_df))
        
        metrics = {
            "Total Pipeline Value": f"₹{total_val:,.2f}",
            "Highest Revenue Sector": top_sector,
            "Delayed Work Orders": delayed,
            "Data Source": data_source_label
        }
        
        summary = self.generator.generate_leadership_summary(metrics, "None detected")
        return summary
