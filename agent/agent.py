import pandas as pd
from integrations.monday_api import MondayClient
from processing import data_cleaner, metrics_engine
from agent.query_interpreter import QueryInterpreter
from agent.insight_generator import InsightGenerator

class BIAgent:
    def __init__(self):
        self.monday = MondayClient()
        self.interpreter = QueryInterpreter()
        self.generator = InsightGenerator()
        
    def _fetch_all_data(self):
        """Fetch and clean data from both boards."""
        try:
            deals_df = self.monday.get_deals_board_data()
            work_orders_df = self.monday.get_work_orders_board_data()
        except Exception as e:
            print(f"Monday API Error: {e}")
            deals_df = pd.DataFrame()
            work_orders_df = pd.DataFrame()

        # Fallback to CSV if empty (for prototype demo)
        if deals_df.empty:
            deals_df = pd.read_csv('data/Deal_funnel_Data.csv')
        if work_orders_df.empty:
            work_orders_df = pd.read_csv('data/Work_Order_Tracker_Data.csv')

        # Cleaning Deals
        deals_df = data_cleaner.normalize_dates(deals_df, ['Close Date (A)', 'Tentative Close Date', 'Created Date'])
        deals_df = data_cleaner.clean_financial_columns(deals_df, ['Masked Deal value'])
        deals_df = data_cleaner.standardize_sector_names(deals_df, 'Sector/service')
        deals_df = data_cleaner.fill_missing_values(deals_df)

        # Cleaning Work Orders
        work_orders_df = data_cleaner.normalize_dates(work_orders_df, ['Probable Start Date', 'Probable End Date', 'Data Delivery Date'])
        work_orders_df = data_cleaner.clean_financial_columns(work_orders_df, ['Amount in Rupees (Incl of GST) (Masked)'])
        work_orders_df = data_cleaner.standardize_sector_names(work_orders_df, 'Sector')
        work_orders_df = data_cleaner.fill_missing_values(work_orders_df)

        return deals_df, work_orders_df

    def process_query(self, user_query):
        """Main orchidstrator flow."""
        # 1. Interpret Query
        intent = self.interpreter.interpret(user_query)
        
        # 2. Get Data
        deals_df, wo_df = self._fetch_all_data()
        
        # 3. Detect Quality Issues
        quality_issues = data_cleaner.detect_data_quality_issues(deals_df if intent['board_source'] == 'deals' else wo_df)
        
        # 4. Calculate Specific Metrics based on intent
        result_metric = "No data found for this query."
        metric_type = intent['metric']
        sector = intent['sector']
        
        target_df = deals_df if intent['board_source'] == 'deals' else wo_df
        if sector != 'all':
            target_df = target_df[target_df['normalized_sector'] == sector.capitalize()]

        if metric_type == 'pipeline_value':
            val = metrics_engine.calculate_pipeline_value(target_df, 'Masked Deal value', 'Deal Status')
            result_metric = f"Total Pipeline Value: ${val:,.2f}"
        elif metric_type == 'revenue_by_sector':
            rev = metrics_engine.revenue_by_sector(target_df, 'Masked Deal value')
            result_metric = rev.to_dict()
        elif metric_type == 'delayed_projects':
            delayed = metrics_engine.detect_delayed_projects(target_df, 'Probable End Date', 'Execution Status')
            result_metric = f"Delayed Projects: {len(delayed)}"
        elif metric_type == 'completion_rate':
            rate = metrics_engine.work_order_completion_rate(target_df, 'Execution Status')
            result_metric = f"Completion Rate: {rate:.1f}%"
        elif metric_type == 'workload':
            workload = metrics_engine.get_operational_workload(target_df)
            result_metric = workload.to_dict()

        # 5. Generate Insight
        insight = self.generator.generate_insight(intent, result_metric, quality_issues)
        
        return {
            "intent": intent,
            "metric_data": result_metric,
            "insight": insight,
            "quality_issues": quality_issues
        }

    def get_weekly_summary(self):
        """Generate high level dashboard summary."""
        deals_df, wo_df = self._fetch_all_data()
        
        total_pipeline = metrics_engine.calculate_pipeline_value(deals_df, 'Masked Deal value', 'Deal Status')
        top_sector = metrics_engine.revenue_by_sector(deals_df, 'Masked Deal value').index[0]
        delayed = len(metrics_engine.detect_delayed_projects(wo_df, 'Probable End Date', 'Execution Status'))
        
        metrics = {
            "Pipeline Value": f"${total_pipeline:,.2f}",
            "Top Sector": top_sector,
            "Delayed Projects": delayed
        }
        
        risks = data_cleaner.detect_data_quality_issues(deals_df) + data_cleaner.detect_data_quality_issues(wo_df)
        
        summary = self.generator.generate_leadership_summary(metrics, risks)
        return summary
