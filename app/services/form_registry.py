"""
Master registry of all official government court form URLs.
All 5 features × all 50 states + DC + Federal.
Used by the form fetcher to know what to download and cache.
"""

# Structure: { "feature_key": { "State": [("filename.pdf", "https://url")] } }

FORM_REGISTRY = {

    # ══════════════════════════════════════════════════════════════
    # FEATURE 1 — DIVORCE PETITION FORMS
    # ══════════════════════════════════════════════════════════════
    "01_divorce": {
        "Alabama": [("AL_divorce_complaint.pdf","https://eforms.alacourt.gov/media/lmgc2trw/divorce-complaint.pdf"),("AL_uncontested_divorce_packet.pdf","https://eforms.alacourt.gov/media/ah3bv32s/uncontested-divorce-packet.pdf"),("AL_final_judgment_divorce.pdf","https://eforms.alacourt.gov/media/jzndukam/final-judgment-of-divorce.pdf")],
        "Alaska": [("AK_dissolution_with_children.pdf","https://public.courts.alaska.gov/web/forms/docs/dr-1total.pdf"),("AK_dissolution_no_children.pdf","https://public.courts.alaska.gov/web/forms/docs/dr-2total.pdf"),("AK_divorce_no_children_complaint.pdf","https://courts.alaska.gov/shc/family/docs/shc-111n.pdf")],
        "Arizona": [("AZ_divorce_petition.pdf","https://www.azcourts.gov/Portals/0/31/Forms/AOCDR10H.pdf")],
        "Arkansas": [("AR_divorce_complaint.pdf","https://www.arcourts.gov/sites/default/files/ComplaintForDivorce.pdf")],
        "California": [("CA_FL100_petition.pdf","https://www.courts.ca.gov/documents/fl100.pdf"),("CA_FL110_summons.pdf","https://www.courts.ca.gov/documents/fl110.pdf"),("CA_FL120_response.pdf","https://www.courts.ca.gov/documents/fl120.pdf"),("CA_FL150_financial.pdf","https://www.courts.ca.gov/documents/fl150.pdf"),("CA_FL180_judgment.pdf","https://www.courts.ca.gov/documents/fl180.pdf")],
        "Colorado": [("CO_JDF1000_petition.pdf","https://www.courts.state.co.us/userfiles/file/Court_Probation/Self_Help/Forms/Family_Law/JDF%201000%20R10-21%20Petition%20for%20Dissolution%20of%20Marriage%20or%20Legal%20Separation.pdf")],
        "Connecticut": [("CT_FM159_divorce.pdf","https://www.jud.ct.gov/webforms/forms/fm159.pdf"),("CT_FM75_financial.pdf","https://www.jud.ct.gov/webforms/forms/fm075.pdf")],
        "Delaware": [("DE_divorce_petition.pdf","https://courts.delaware.gov/forms/download.aspx?id=39354")],
        "Florida": [("FL_12901a_petition.pdf","https://www.flcourts.gov/content/download/405428/file/12.901(a).pdf"),("FL_12902b_financial.pdf","https://www.flcourts.gov/content/download/405439/file/12.902(b)(1).pdf"),("FL_12930a_summons.pdf","https://www.flcourts.gov/content/download/405447/file/12.930(a).pdf")],
        "Georgia": [("GA_divorce_petition.pdf","https://georgiacourts.gov/wp-content/uploads/2020/11/Petition-for-Divorce-fillable.pdf"),("GA_financial_affidavit.pdf","https://georgiacourts.gov/wp-content/uploads/2020/11/Domestic-Relations-Financial-Affidavit.pdf"),("GA_child_support.pdf","https://georgiacourts.gov/wp-content/uploads/2021/01/Child-Support-Worksheet.pdf")],
        "Hawaii": [("HI_divorce_complaint.pdf","https://www.courts.state.hi.us/docs/form/famcrt/1F-P-924.pdf")],
        "Idaho": [("ID_divorce_complaint.pdf","https://isc.idaho.gov/forms-repository/CAO%20FLP%201-1.pdf"),("ID_financial_statement.pdf","https://isc.idaho.gov/forms-repository/CAO%20FLP%201-7.pdf")],
        "Illinois": [("IL_petition_dissolution.pdf","https://www.illinoiscourts.gov/resources/b73faf5e-1eb7-4eb8-b9a0-8d37af18e9af/file")],
        "Indiana": [("IN_divorce_petition.pdf","https://www.in.gov/courts/files/petition-for-dissolution.pdf")],
        "Iowa": [("IA_divorce_petition.pdf","https://www.iowacourts.gov/media/cms/Petition_for_Dissolution_of_Marr_1D1A5C9B45A18.pdf")],
        "Kansas": [("KS_divorce_petition.pdf","https://www.kscourts.org/KSCourts/media/KsCourts/Forms/Divorce/Petition-for-Divorce.pdf")],
        "Kentucky": [("KY_dissolution_petition.pdf","https://kycourts.gov/Legal-Help/Documents/Petition%20for%20Dissolution%20of%20Marriage.pdf")],
        "Louisiana": [("LA_divorce_petition.pdf","https://www.lasc.org/rules/dist.ct/Appendix8.0.pdf")],
        "Maine": [("ME_divorce_complaint.pdf","https://www.courts.maine.gov/fees_forms/forms/CV-divorce-complaint.pdf")],
        "Maryland": [("MD_CCDR020_complaint.pdf","https://www.courts.state.md.us/sites/default/files/import/family/forms/ccdr020.pdf"),("MD_CCDR030_financial.pdf","https://www.courts.state.md.us/sites/default/files/import/family/forms/ccdr030.pdf")],
        "Massachusetts": [("MA_CJD200_joint_petition.pdf","https://www.mass.gov/doc/cjd200/download"),("MA_CJD101a_complaint.pdf","https://www.mass.gov/doc/complaint-for-divorce-cjd-101a/download")],
        "Michigan": [("MI_DC100_complaint.pdf","https://courts.michigan.gov/Administration/SCAO/Forms/courtforms/dc100.pdf")],
        "Minnesota": [("MN_divorce_petition.pdf","https://www.mncourts.gov/mncourtsgov/media/CourtForms/FAM101.pdf"),("MN_financial_disclosure.pdf","https://www.mncourts.gov/mncourtsgov/media/CourtForms/FAM111.pdf")],
        "Mississippi": [("MS_complaint_divorce.pdf","https://courts.ms.gov/research/forms/chancery/ComplaintForDivorce.pdf")],
        "Missouri": [("MO_petition_dissolution.pdf","https://www.courts.mo.gov/file.jsp?id=3306")],
        "Montana": [("MT_divorce_petition.pdf","https://courts.mt.gov/Portals/189/forms/family/petition_dissolution.pdf")],
        "Nebraska": [("NE_complaint_dissolution.pdf","https://supremecourt.nebraska.gov/sites/default/files/CH6-10.pdf")],
        "Nevada": [("NV_divorce_complaint.pdf","https://www.nevadajudiciary.us/images/CommitteeMaterials/FamilyLaw/forms/Complaint-for-Divorce.pdf")],
        "New Hampshire": [("NH_divorce_petition.pdf","https://www.courts.nh.gov/sites/g/files/ehbemt471/files/documents/2020-12/nhjb-2070-dfe.pdf")],
        "New Jersey": [("NJ_complaint_divorce.pdf","https://www.njcourts.gov/forms/10153_divorce_complnt.pdf"),("NJ_CIS_financial.pdf","https://www.njcourts.gov/forms/10144_cis.pdf")],
        "New Mexico": [("NM_4A_petition.pdf","https://nmcourts.gov/wp-content/uploads/2022/08/4A-201.pdf")],
        "New York": [("NY_UD1_summons.pdf","https://www.nycourts.gov/divorce/forms/ud-1.pdf"),("NY_UD2_complaint.pdf","https://www.nycourts.gov/divorce/forms/ud-2.pdf"),("NY_UD6_affidavit.pdf","https://www.nycourts.gov/divorce/forms/ud-6.pdf"),("NY_UD9_financial.pdf","https://www.nycourts.gov/divorce/forms/ud-9.pdf"),("NY_UD10_note_of_issue.pdf","https://www.nycourts.gov/divorce/forms/ud-10.pdf")],
        "North Carolina": [("NC_divorce_complaint.pdf","https://www.nccourts.gov/assets/inline-files/Civil-Summons-AOC-CV-100.pdf")],
        "North Dakota": [("ND_divorce_packet.pdf","https://www.ndcourts.gov/Media/Default/Legal%20Self%20Help/Family%20Law/Packet_Divorce_No_Children.pdf")],
        "Ohio": [("OH_divorce_complaint.pdf","https://www.supremecourt.ohio.gov/JCS/CFC/Resources/Forms/divorce_dissolution/complaint_for_divorce.pdf")],
        "Oklahoma": [("OK_petition_dissolution.pdf","https://www.oscn.net/static/oscn/content/rules/forms/petition_for_divorce.pdf")],
        "Oregon": [("OR_dissolution_petition.pdf","https://www.courts.oregon.gov/forms/Documents/DR201.pdf")],
        "Pennsylvania": [("PA_divorce_complaint.pdf","https://www.pacourts.us/assets/files/setting-5571/file-5636.pdf")],
        "Rhode Island": [("RI_divorce_complaint.pdf","https://www.courts.ri.gov/PublicResources/forms/Family%20Court%20Forms/Complaint%20for%20Divorce%20No%20Children.pdf")],
        "South Carolina": [("SC_divorce_summons.pdf","https://www.sccourts.org/forms/pdf/SCCA401.pdf"),("SC_financial_declaration.pdf","https://www.sccourts.org/forms/pdf/SCCA400.pdf")],
        "South Dakota": [("SD_divorce_complaint.pdf","https://ujs.sd.gov/uploads/forms/UJS-003.pdf")],
        "Tennessee": [("TN_divorce_complaint.pdf","https://www.tncourts.gov/sites/default/files/docs/complaint_for_divorce_0.pdf")],
        "Texas": [("TX_divorce_petition.pdf","https://www.txcourts.gov/media/1446848/original-petition-for-divorce.pdf"),("TX_waiver_citation.pdf","https://www.txcourts.gov/media/1446852/waiver-of-citation.pdf"),("TX_final_decree.pdf","https://www.txcourts.gov/media/1446856/final-decree-of-divorce.pdf")],
        "Utah": [("UT_complaint_divorce.pdf","https://www.utcourts.gov/howto/divorce/docs/1100fa.pdf"),("UT_financial_declaration.pdf","https://www.utcourts.gov/howto/divorce/docs/1112fa.pdf")],
        "Vermont": [("VT_divorce_complaint.pdf","https://www.vermontjudiciary.org/sites/default/files/documents/100-00250_Complaint_for_Divorce_or_Legal_Separation_fillable.pdf")],
        "Virginia": [("VA_divorce_complaint.pdf","https://www.courts.state.va.us/forms/district/dc-510.pdf")],
        "Washington": [("WA_petition_divorce.pdf","https://www.courts.wa.gov/forms/documents/DR01_0900_Pet4Dis.pdf"),("WA_summons.pdf","https://www.courts.wa.gov/forms/documents/DR01_0200_Summons.pdf")],
        "West Virginia": [("WV_divorce_petition.pdf","https://www.courtswv.gov/public-resources/court-forms/family-court/SFF-Family-Court-Petition.pdf")],
        "Wisconsin": [("WI_FA4001_petition.pdf","https://www.wicourts.gov/formdisplay/FA-4001V.pdf"),("WI_FA4139_financial.pdf","https://www.wicourts.gov/formdisplay/FA-4139.pdf")],
        "Wyoming": [("WY_divorce_complaint.pdf","https://www.courts.state.wy.us/wp-content/uploads/2017/07/Complaint-for-Divorce.pdf")],
        "Washington DC": [("DC_complaint_divorce.pdf","https://www.dccourts.gov/sites/default/files/2021-12/Complaint-for-Absolute-Divorce.pdf")],
    },

    # ══════════════════════════════════════════════════════════════
    # FEATURE 2 — NAME CHANGE FORMS
    # ══════════════════════════════════════════════════════════════
    "02_name_change": {
        "_FEDERAL": [("SSA_SS5.pdf","https://www.ssa.gov/forms/ss-5.pdf"),("DS5504_passport_name_change.pdf","https://eforms.state.gov/Forms/ds5504.pdf"),("DS82_passport_renewal.pdf","https://eforms.state.gov/Forms/ds82.pdf"),("DS11_new_passport.pdf","https://eforms.state.gov/Forms/ds11.pdf")],
        "Alabama": [("AL_DMV_MV9.pdf","https://www.alabamadmv.org/wp-content/uploads/2019/01/MV-9.pdf")],
        "Alaska": [("AK_DMV_478.pdf","https://www.dmv.alaska.gov/dmv/forms/pdfs/478.pdf")],
        "Arizona": [("AZ_DMV_960236.pdf","https://azdot.gov/sites/default/files/media/96-0236.pdf")],
        "Arkansas": [("AR_DMV_DL1.pdf","https://www.dfa.arkansas.gov/images/uploads/motorVehicleOffice/DL1.pdf")],
        "California": [("CA_DMV_DL44.pdf","https://www.dmv.ca.gov/portal/uploads/2020/05/dl44.pdf")],
        "Colorado": [("CO_DMV_name_change_instructions.pdf","https://dmv.colorado.gov/update-change-manage-your-name-your-credential")],
        "Connecticut": [("CT_DMV_B230.pdf","https://portal.ct.gov/-/media/DMV/Forms/B-230.pdf")],
        "Delaware": [("DE_DMV_MV212.pdf","https://www.dmv.de.gov/sites/default/files/pdf/forms/MV212.pdf")],
        "Florida": [("FL_DMV_HSMV72010.pdf","https://www.flhsmv.gov/pdf/forms/72010.pdf")],
        "Georgia": [("GA_DMV_DS1.pdf","https://dds.georgia.gov/sites/dds.georgia.gov/files/related_files/site_page/DS-1%20Application%20for%20Georgia%20Drivers%20License%20or%20ID%20Card.pdf")],
        "Hawaii": [("HI_DMV_MVMO14.pdf","https://hidot.hawaii.gov/highways/files/2014/12/mvmo-form14.pdf")],
        "Idaho": [("ID_DMV_ITD3368.pdf","https://itd.idaho.gov/wp-content/uploads/2016/07/itd3368.pdf")],
        "Illinois": [("IL_DMV_DSD_A100.pdf","https://www.ilsos.gov/publications/pdf_publications/dsd_a100.pdf")],
        "Indiana": [("IN_BMV_SF54057.pdf","https://www.in.gov/bmv/files/SF54057.pdf")],
        "Iowa": [("IA_DOT_431120.pdf","https://iowadot.gov/mvd/realid/forms/431120.pdf")],
        "Kansas": [("KS_DMV_TR720.pdf","https://www.ksrevenue.gov/pdf/TR-720.pdf")],
        "Kentucky": [("KY_TC96182.pdf","https://drive.ky.gov/motor-vehicle-licensing/Documents/TC%2096-182.pdf")],
        "Louisiana": [("LA_DPSMV1799.pdf","https://www.dps.louisiana.gov/assets/docs/OMV/forms/dpsmv1799.pdf")],
        "Maine": [("ME_DMV_MV45.pdf","https://www.maine.gov/sos/bmv/licenses/documents/MV-45.pdf")],
        "Maryland": [("MD_MVA_VR234.pdf","https://mva.maryland.gov/Documents/VR-234.pdf")],
        "Massachusetts": [("MA_RMV_name_change.pdf","https://www.mass.gov/doc/name-change-instructions/download")],
        "Michigan": [("MI_SOS_DL_application.pdf","https://www.michigan.gov/documents/sos/SOS_DL_Application_372403_7.pdf")],
        "Minnesota": [("MN_DVS_PS33900.pdf","https://dps.mn.gov/divisions/dvs/forms-documents/Documents/PS33900_Driver_License_Application.pdf")],
        "Mississippi": [("MS_DPS_78015.pdf","https://www.dps.state.ms.us/wp-content/uploads/78-015-App-for-Mississippi-DL-or-ID.pdf")],
        "Missouri": [("MO_DOR_108.pdf","https://dor.mo.gov/forms/108.pdf")],
        "Montana": [("MT_MV8.pdf","https://doj.mt.gov/wp-content/uploads/sites/88/2021/04/mv8_app.pdf")],
        "Nebraska": [("NE_DMV_6007.pdf","https://dmv.nebraska.gov/sites/dmv.nebraska.gov/files/doc/dvr/6007AppForOperatorsLicense.pdf")],
        "Nevada": [("NV_DMV_VP016.pdf","https://dmv.nv.gov/Forms/VP016/")],
        "New Hampshire": [("NH_DSMV450.pdf","https://www.nh.gov/safety/divisions/dmv/forms/documents/dsmv450.pdf")],
        "New Jersey": [("NJ_MVC_BA208.pdf","https://www.state.nj.us/mvc/pdf/BA-208.pdf")],
        "New Mexico": [("NM_MVD_10005.pdf","https://www.mvd.newmexico.gov/forms/mvd-10005.pdf")],
        "New York": [("NY_DMV_MV44.pdf","https://dmv.ny.gov/sites/default/files/doc/mv44.pdf")],
        "North Carolina": [("NC_DMV_DL101A.pdf","https://www.ncdot.gov/dmv/license-id/drivers-license/Documents/DL-101A.pdf")],
        "North Dakota": [("ND_DOT_SFN51403.pdf","https://www.dot.nd.gov/forms/sfn51403.pdf")],
        "Ohio": [("OH_BMV_2016.pdf","https://www.bmv.ohio.gov/static/forms/bmv2016.pdf")],
        "Oklahoma": [("OK_DPS_761.pdf","https://www.ok.gov/dps/documents/Driver_License_Application_761_(05-09-16).pdf")],
        "Oregon": [("OR_DMV_735173.pdf","https://www.oregon.gov/odot/DMV/docs/735-173.pdf")],
        "Pennsylvania": [("PA_DMV_DL54A.pdf","https://www.dmv.pa.gov/FORMS/Form%20DL-54A.pdf")],
        "Rhode Island": [("RI_DMV_LIC001.pdf","https://www.dmv.ri.gov/documents/forms/license/LIC001.pdf")],
        "South Carolina": [("SC_DMV_447W.pdf","https://www.scdmvonline.com/DMVNew/forms/447W.pdf")],
        "South Dakota": [("SD_DMV_MV100.pdf","https://dor.sd.gov/Taxes/Business_Taxes/Motor_Vehicle/Documents/MV_Forms/MV-100.pdf")],
        "Tennessee": [("TN_DOS_SF0461.pdf","https://www.tn.gov/content/dam/tn/safety/documents/sf0461.pdf")],
        "Texas": [("TX_DPS_DL14A.pdf","https://www.dps.texas.gov/internetforms/Forms/DL-14A.pdf")],
        "Utah": [("UT_DMV_DLD3.pdf","https://dld.utah.gov/wp-content/uploads/sites/17/2020/02/DLD3.pdf")],
        "Vermont": [("VT_DMV_VL021.pdf","https://dmv.vermont.gov/sites/dmv/files/documents/forms/VL021.pdf")],
        "Virginia": [("VA_DMV_DL1P.pdf","https://www.dmv.virginia.gov/webdoc/pdf/dl1p.pdf")],
        "Washington": [("WA_DOL_420001.pdf","https://www.dol.wa.gov/forms/420001.pdf")],
        "West Virginia": [("WV_DMV_DL201.pdf","https://transportation.wv.gov/DMV/Forms/Documents/DL201.pdf")],
        "Wisconsin": [("WI_DMV_MV3001.pdf","https://wisconsindot.gov/Documents/formdocs/mv3001.pdf")],
        "Wyoming": [("WY_DOT_MV100.pdf","https://www.dot.state.wy.us/files/live/sites/wydot/files/shared/MV/Forms/WYDOT_MV100.pdf")],
        "Washington DC": [("DC_DMV_application.pdf","https://dmv.dc.gov/sites/default/files/dc/sites/dmv/publication/attachments/DC_DMV_App_DL_NonDriver_ID.pdf")],
    },

    # ══════════════════════════════════════════════════════════════
    # FEATURE 3 — ASSET TRANSFER FORMS
    # ══════════════════════════════════════════════════════════════
    "03_asset": {
        "_FEDERAL": [("IRS_Pub575_pension.pdf","https://www.irs.gov/pub/irs-pdf/p575.pdf"),("DOL_QDRO_guide.pdf","https://www.dol.gov/sites/dolgov/files/ebsa/about-ebsa/our-activities/resource-center/publications/qdros-the-division-of-retirement-benefits-through-qualified-domestic-relations-orders.pdf")],
        "Alabama": [("AL_uncontested_divorce_packet.pdf","https://eforms.alacourt.gov/media/ah3bv32s/uncontested-divorce-packet.pdf")],
        "Alaska": [("AK_property_division.pdf","https://public.courts.alaska.gov/web/forms/docs/dr-2total.pdf")],
        "Arizona": [("AZ_DR45_financial.pdf","https://www.azcourts.gov/Portals/0/31/Forms/AOCDR45H.pdf"),("AZ_DR65_property.pdf","https://www.azcourts.gov/Portals/0/31/Forms/AOCDR65H.pdf")],
        "Arkansas": [("AR_property_settlement.pdf","https://www.arcourts.gov/sites/default/files/PropertySettlementAgreement.pdf")],
        "California": [("CA_FL160_property.pdf","https://www.courts.ca.gov/documents/fl160.pdf"),("CA_FL142_asset_debt.pdf","https://www.courts.ca.gov/documents/fl142.pdf"),("CA_FL150_income.pdf","https://www.courts.ca.gov/documents/fl150.pdf")],
        "Colorado": [("CO_JDF1104_financial.pdf","https://www.courts.state.co.us/userfiles/file/Court_Probation/Self_Help/Forms/Family_Law/JDF%201104%20R7-20%20Sworn%20Financial%20Statement.pdf"),("CO_JDF1115_separation.pdf","https://www.courts.state.co.us/userfiles/file/Court_Probation/Self_Help/Forms/Family_Law/JDF%201115%20R7-20%20Separation%20Agreement.pdf")],
        "Connecticut": [("CT_FM75_financial.pdf","https://www.jud.ct.gov/webforms/forms/fm075.pdf"),("CT_FM183_property.pdf","https://www.jud.ct.gov/webforms/forms/fm183.pdf")],
        "Delaware": [("DE_property_division.pdf","https://courts.delaware.gov/forms/download.aspx?id=39356")],
        "Florida": [("FL_12902b2_financial.pdf","https://www.flcourts.gov/content/download/405440/file/12.902(b)(2).pdf"),("FL_12902j_assets.pdf","https://www.flcourts.gov/content/download/405445/file/12.902(j).pdf")],
        "Georgia": [("GA_financial_affidavit.pdf","https://georgiacourts.gov/wp-content/uploads/2020/11/Domestic-Relations-Financial-Affidavit.pdf"),("GA_settlement_agreement.pdf","https://georgiacourts.gov/wp-content/uploads/2020/11/Settlement-Agreement-fillable.pdf")],
        "Hawaii": [("HI_property_division.pdf","https://www.courts.state.hi.us/docs/form/famcrt/1F-P-926.pdf")],
        "Idaho": [("ID_property_settlement.pdf","https://isc.idaho.gov/forms-repository/CAO%20FLP%201-9.pdf")],
        "Illinois": [("IL_financial_affidavit.pdf","https://www.illinoiscourts.gov/resources/a3c65b9b-eef1-4a2c-9d50-5df3c8b5d8d1/file")],
        "Indiana": [("IN_property_settlement.pdf","https://www.in.gov/courts/files/property-settlement-agreement.pdf")],
        "Iowa": [("IA_financial_affidavit.pdf","https://www.iowacourts.gov/media/cms/Financial_Affidavit_1D1A5C9B45A20.pdf")],
        "Kansas": [("KS_financial_affidavit.pdf","https://www.kscourts.org/KSCourts/media/KsCourts/Forms/Divorce/Financial-Affidavit.pdf")],
        "Kentucky": [("KY_financial_disclosure.pdf","https://kycourts.gov/Legal-Help/Documents/Financial%20Disclosure%20Statement.pdf")],
        "Louisiana": [("LA_community_property.pdf","https://www.lasc.org/rules/dist.ct/Appendix9.0.pdf")],
        "Maine": [("ME_financial_statement.pdf","https://www.courts.maine.gov/fees_forms/forms/FM-financial-statement.pdf")],
        "Maryland": [("MD_financial_statement.pdf","https://www.courts.state.md.us/sites/default/files/import/family/forms/ccdr030.pdf")],
        "Massachusetts": [("MA_financial_statement.pdf","https://www.mass.gov/doc/financial-statement-short-form-cjd301s/download")],
        "Michigan": [("MI_FOC10.pdf","https://courts.michigan.gov/Administration/SCAO/Forms/courtforms/foc10.pdf"),("MI_property_settlement.pdf","https://courts.michigan.gov/Administration/SCAO/Forms/courtforms/dc84.pdf")],
        "Minnesota": [("MN_financial_disclosure.pdf","https://www.mncourts.gov/mncourtsgov/media/CourtForms/FAM111.pdf"),("MN_settlement_agreement.pdf","https://www.mncourts.gov/mncourtsgov/media/CourtForms/FAM116.pdf")],
        "Mississippi": [("MS_property_settlement.pdf","https://courts.ms.gov/research/forms/chancery/PropertySettlementAgreement.pdf")],
        "Missouri": [("MO_financial_statement.pdf","https://www.courts.mo.gov/file.jsp?id=3310")],
        "Montana": [("MT_property_settlement.pdf","https://courts.mt.gov/Portals/189/forms/family/separation_agreement.pdf")],
        "Nebraska": [("NE_property_settlement.pdf","https://supremecourt.nebraska.gov/sites/default/files/CH6-14.pdf")],
        "Nevada": [("NV_financial_disclosure.pdf","https://www.nevadajudiciary.us/images/CommitteeMaterials/FamilyLaw/forms/Financial-Disclosure-Form.pdf")],
        "New Hampshire": [("NH_financial_affidavit.pdf","https://www.courts.nh.gov/sites/g/files/ehbemt471/files/documents/2020-12/nhjb-2065-dfe.pdf")],
        "New Jersey": [("NJ_CIS_financial.pdf","https://www.njcourts.gov/forms/10144_cis.pdf")],
        "New Mexico": [("NM_financial_disclosure.pdf","https://nmcourts.gov/wp-content/uploads/2022/08/4A-212.pdf")],
        "New York": [("NY_UD8_settlement.pdf","https://www.nycourts.gov/divorce/forms/ud-8.pdf"),("NY_net_worth.pdf","https://www.nycourts.gov/forms/matrimonial/networth.pdf")],
        "North Carolina": [("NC_financial_affidavit.pdf","https://www.nccourts.gov/assets/inline-files/Family-Law-Financial-Affidavit-AOC-CV-613.pdf")],
        "North Dakota": [("ND_property_settlement.pdf","https://www.ndcourts.gov/Media/Default/Legal%20Self%20Help/Family%20Law/Property_Settlement_Agreement.pdf")],
        "Ohio": [("OH_separation_agreement.pdf","https://www.supremecourt.ohio.gov/JCS/CFC/Resources/Forms/divorce_dissolution/separation_agreement.pdf")],
        "Oklahoma": [("OK_property_settlement.pdf","https://www.oscn.net/static/oscn/content/rules/forms/property_settlement_agreement.pdf")],
        "Oregon": [("OR_property_agreement.pdf","https://www.courts.oregon.gov/forms/Documents/DR405.pdf")],
        "Pennsylvania": [("PA_financial_statement.pdf","https://www.pacourts.us/assets/files/setting-5571/file-5640.pdf")],
        "Rhode Island": [("RI_property_settlement.pdf","https://www.courts.ri.gov/PublicResources/forms/Family%20Court%20Forms/Property%20Settlement%20Agreement.pdf")],
        "South Carolina": [("SC_financial_declaration.pdf","https://www.sccourts.org/forms/pdf/SCCA400.pdf")],
        "South Dakota": [("SD_property_settlement.pdf","https://ujs.sd.gov/uploads/forms/UJS-005.pdf")],
        "Tennessee": [("TN_marital_dissolution.pdf","https://www.tncourts.gov/sites/default/files/docs/marital_dissolution_agreement.pdf")],
        "Texas": [("TX_inventory.pdf","https://www.txcourts.gov/media/1446862/inventory-and-appraisement.pdf"),("TX_agreed_decree.pdf","https://www.txcourts.gov/media/1446858/agreed-decree-of-divorce.pdf")],
        "Utah": [("UT_financial_declaration.pdf","https://www.utcourts.gov/howto/divorce/docs/1112fa.pdf")],
        "Vermont": [("VT_property_agreement.pdf","https://www.vermontjudiciary.org/sites/default/files/documents/100-00265_Stipulation_and_Order_fillable.pdf")],
        "Virginia": [("VA_property_settlement.pdf","https://www.courts.state.va.us/forms/circuit/cc1406.pdf")],
        "Washington": [("WA_separation_agreement.pdf","https://www.courts.wa.gov/forms/documents/DR01_0700_SepContrPropAgr.pdf"),("WA_financial_declaration.pdf","https://www.courts.wa.gov/forms/documents/DR01_0550_FinDeclaration.pdf")],
        "West Virginia": [("WV_marital_settlement.pdf","https://www.courtswv.gov/public-resources/court-forms/family-court/SFF-Marital-Settlement-Agreement.pdf")],
        "Wisconsin": [("WI_FA4150_settlement.pdf","https://www.wicourts.gov/formdisplay/FA-4150.pdf")],
        "Wyoming": [("WY_property_settlement.pdf","https://www.courts.state.wy.us/wp-content/uploads/2017/07/Property-Settlement-Agreement.pdf")],
        "Washington DC": [("DC_financial_statement.pdf","https://www.dccourts.gov/sites/default/files/2021-12/Financial-Statement.pdf")],
    },

    # ══════════════════════════════════════════════════════════════
    # FEATURE 4 — CO-PARENTING PLAN FORMS
    # ══════════════════════════════════════════════════════════════
    "04_coparenting": {
        "Alabama": [("AL_uncontested_divorce_packet.pdf","https://eforms.alacourt.gov/media/ah3bv32s/uncontested-divorce-packet.pdf")],
        "Alaska": [("AK_parenting_plan.pdf","https://public.courts.alaska.gov/web/forms/docs/dr-1total.pdf"),("AK_child_support.pdf","https://courts.alaska.gov/shc/family/docs/shc-1100n.pdf")],
        "Arizona": [("AZ_DR35_parenting_plan.pdf","https://www.azcourts.gov/Portals/0/31/Forms/AOCDR35H.pdf"),("AZ_DR40_child_support.pdf","https://www.azcourts.gov/Portals/0/31/Forms/AOCDR40H.pdf")],
        "Arkansas": [("AR_custody_order.pdf","https://www.arcourts.gov/sites/default/files/CustodyOrder.pdf")],
        "California": [("CA_FL341_parenting_plan.pdf","https://www.courts.ca.gov/documents/fl341.pdf"),("CA_FL342_child_support.pdf","https://www.courts.ca.gov/documents/fl342.pdf"),("CA_FL311_custody.pdf","https://www.courts.ca.gov/documents/fl311.pdf")],
        "Colorado": [("CO_JDF1113_parenting.pdf","https://www.courts.state.co.us/userfiles/file/Court_Probation/Self_Help/Forms/Family_Law/JDF%201113%20R7-20%20Parenting%20Plan.pdf"),("CO_JDF1818_child_support.pdf","https://www.courts.state.co.us/userfiles/file/Court_Probation/Self_Help/Forms/Family_Law/JDF%201818%20R10-21%20Child%20Support%20Worksheet.pdf")],
        "Connecticut": [("CT_FM183_parenting.pdf","https://www.jud.ct.gov/webforms/forms/fm183.pdf"),("CT_FM084_child_support.pdf","https://www.jud.ct.gov/webforms/forms/fm084.pdf")],
        "Delaware": [("DE_parenting_plan.pdf","https://courts.delaware.gov/forms/download.aspx?id=39358")],
        "Florida": [("FL_12995a_parenting.pdf","https://www.flcourts.gov/content/download/405460/file/12.995(a).pdf"),("FL_12902e_child_support.pdf","https://www.flcourts.gov/content/download/405443/file/12.902(e).pdf")],
        "Georgia": [("GA_parenting_plan.pdf","https://georgiacourts.gov/wp-content/uploads/2020/11/Parenting-Plan-Order-fillable.pdf"),("GA_child_support.pdf","https://georgiacourts.gov/wp-content/uploads/2021/01/Child-Support-Worksheet.pdf")],
        "Hawaii": [("HI_parenting_plan.pdf","https://www.courts.state.hi.us/docs/form/famcrt/1F-P-930.pdf")],
        "Idaho": [("ID_parenting_plan.pdf","https://isc.idaho.gov/forms-repository/CAO%20FLP%201-11.pdf")],
        "Illinois": [("IL_parenting_plan.pdf","https://www.illinoiscourts.gov/resources/f34eb48f-aba0-4a4a-8ecc-c19f7e675a97/file")],
        "Indiana": [("IN_parenting_guidelines.pdf","https://www.in.gov/courts/files/parenting-time-guidelines.pdf")],
        "Iowa": [("IA_parenting_plan.pdf","https://www.iowacourts.gov/media/cms/Parenting_Plan_1D1A5C9B45A22.pdf")],
        "Kansas": [("KS_parenting_plan.pdf","https://www.kscourts.org/KSCourts/media/KsCourts/Forms/Divorce/Parenting-Plan.pdf")],
        "Kentucky": [("KY_parenting_plan.pdf","https://kycourts.gov/Legal-Help/Documents/Parenting%20Plan.pdf")],
        "Louisiana": [("LA_parenting_plan.pdf","https://www.lasc.org/rules/dist.ct/ParentingPlan.pdf")],
        "Maine": [("ME_parenting_plan.pdf","https://www.courts.maine.gov/fees_forms/forms/FM-parenting-plan.pdf")],
        "Maryland": [("MD_parenting_plan.pdf","https://www.courts.state.md.us/sites/default/files/import/family/forms/ccdr056.pdf")],
        "Massachusetts": [("MA_parenting_plan.pdf","https://www.mass.gov/doc/parenting-plan-jd-vl-003/download")],
        "Michigan": [("MI_FOC10_parenting.pdf","https://courts.michigan.gov/Administration/SCAO/Forms/courtforms/foc10.pdf"),("MI_FOC23_child_support.pdf","https://courts.michigan.gov/Administration/SCAO/Forms/courtforms/foc23.pdf")],
        "Minnesota": [("MN_parenting_plan.pdf","https://www.mncourts.gov/mncourtsgov/media/CourtForms/FAM302.pdf"),("MN_child_support.pdf","https://www.mncourts.gov/mncourtsgov/media/CourtForms/FAM301.pdf")],
        "Mississippi": [("MS_custody_order.pdf","https://courts.ms.gov/research/forms/chancery/CustodyOrder.pdf")],
        "Missouri": [("MO_parenting_plan.pdf","https://www.courts.mo.gov/file.jsp?id=3312")],
        "Montana": [("MT_parenting_plan.pdf","https://courts.mt.gov/Portals/189/forms/family/parenting_plan.pdf")],
        "Nebraska": [("NE_parenting_plan.pdf","https://supremecourt.nebraska.gov/sites/default/files/CH6-16.pdf")],
        "Nevada": [("NV_parenting_plan.pdf","https://www.nevadajudiciary.us/images/CommitteeMaterials/FamilyLaw/forms/Parenting-Plan.pdf")],
        "New Hampshire": [("NH_parenting_plan.pdf","https://www.courts.nh.gov/sites/g/files/ehbemt471/files/documents/2020-12/nhjb-2063-dfe.pdf")],
        "New Jersey": [("NJ_parenting_plan.pdf","https://www.njcourts.gov/forms/11217_parenting_plan.pdf")],
        "New Mexico": [("NM_parenting_plan.pdf","https://nmcourts.gov/wp-content/uploads/2022/08/4A-220.pdf")],
        "New York": [("NY_V6_custody.pdf","https://www.nycourts.gov/forms/familycourt/pdfs/V6.pdf"),("NY_child_support.pdf","https://www.nycourts.gov/forms/familycourt/pdfs/4-a.pdf")],
        "North Carolina": [("NC_custody_order.pdf","https://www.nccourts.gov/assets/inline-files/Custody-Visitation-AOC-CV-640.pdf")],
        "North Dakota": [("ND_parenting_plan.pdf","https://www.ndcourts.gov/Media/Default/Legal%20Self%20Help/Family%20Law/Parenting_Plan.pdf")],
        "Ohio": [("OH_parenting_plan.pdf","https://www.supremecourt.ohio.gov/JCS/CFC/Resources/Forms/divorce_dissolution/parenting_plan.pdf")],
        "Oklahoma": [("OK_parenting_plan.pdf","https://www.oscn.net/static/oscn/content/rules/forms/parenting_plan.pdf")],
        "Oregon": [("OR_DR454_parenting.pdf","https://www.courts.oregon.gov/forms/Documents/DR454.pdf"),("OR_child_support.pdf","https://www.courts.oregon.gov/forms/Documents/DR505.pdf")],
        "Pennsylvania": [("PA_custody_agreement.pdf","https://www.pacourts.us/assets/files/setting-5571/file-5642.pdf")],
        "Rhode Island": [("RI_parenting_plan.pdf","https://www.courts.ri.gov/PublicResources/forms/Family%20Court%20Forms/Parenting%20Plan.pdf")],
        "South Carolina": [("SC_parenting_plan.pdf","https://www.sccourts.org/forms/pdf/SCCA402.pdf")],
        "South Dakota": [("SD_parenting_plan.pdf","https://ujs.sd.gov/uploads/forms/UJS-007.pdf")],
        "Tennessee": [("TN_parenting_plan.pdf","https://www.tncourts.gov/sites/default/files/docs/permanent_parenting_plan_order_0.pdf")],
        "Texas": [("TX_possession_order.pdf","https://www.txcourts.gov/media/1446870/standard-possession-order.pdf"),("TX_child_support.pdf","https://www.txcourts.gov/media/1446866/child-support-worksheet.pdf")],
        "Utah": [("UT_parenting_plan.pdf","https://www.utcourts.gov/howto/divorce/docs/1128fa.pdf")],
        "Vermont": [("VT_parenting_plan.pdf","https://www.vermontjudiciary.org/sites/default/files/documents/100-00260_Parent_Child_Contact_Order_fillable.pdf")],
        "Virginia": [("VA_parenting_plan.pdf","https://www.courts.state.va.us/forms/circuit/cc1416.pdf")],
        "Washington": [("WA_parenting_plan.pdf","https://www.courts.wa.gov/forms/documents/DR01_0400_PPlan.pdf"),("WA_child_support.pdf","https://www.courts.wa.gov/forms/documents/WSCSS-Worksheets.pdf")],
        "West Virginia": [("WV_parenting_plan.pdf","https://www.courtswv.gov/public-resources/court-forms/family-court/SFF-Parenting-Plan.pdf")],
        "Wisconsin": [("WI_FA4131_parenting.pdf","https://www.wicourts.gov/formdisplay/FA-4131.pdf")],
        "Wyoming": [("WY_parenting_plan.pdf","https://www.courts.state.wy.us/wp-content/uploads/2017/07/Parenting-Plan.pdf")],
        "Washington DC": [("DC_custody_order.pdf","https://www.dccourts.gov/sites/default/files/2021-12/Custody-Order.pdf")],
    },

    # ══════════════════════════════════════════════════════════════
    # FEATURE 5 — FINANCIAL RESET FORMS
    # ══════════════════════════════════════════════════════════════
    "05_financial": {
        "_FEDERAL": [("IRS_W4.pdf","https://www.irs.gov/pub/irs-pdf/fw4.pdf"),("IRS_W4P.pdf","https://www.irs.gov/pub/irs-pdf/fw4p.pdf"),("IRS_8332_child_exemption.pdf","https://www.irs.gov/pub/irs-pdf/f8332.pdf"),("IRS_Pub504_divorced_taxes.pdf","https://www.irs.gov/pub/irs-pdf/p504.pdf"),("IRS_Pub501_filing_status.pdf","https://www.irs.gov/pub/irs-pdf/p501.pdf"),("SSA_survivors_guide.pdf","https://www.ssa.gov/pubs/EN-05-10084.pdf"),("SSA_retirement_benefits.pdf","https://www.ssa.gov/pubs/EN-05-10050.pdf"),("DOL_COBRA_guide.pdf","https://www.dol.gov/sites/dolgov/files/ebsa/about-ebsa/our-activities/resource-center/publications/an-employees-guide-to-health-benefits-under-cobra.pdf"),("DOL_QDRO_guide.pdf","https://www.dol.gov/sites/dolgov/files/ebsa/about-ebsa/our-activities/resource-center/publications/qdros-the-division-of-retirement-benefits-through-qualified-domestic-relations-orders.pdf")],
        "Alabama": [("AL_uncontested_divorce_packet.pdf","https://eforms.alacourt.gov/media/ah3bv32s/uncontested-divorce-packet.pdf")],
        "Alaska": [("AK_financial_disclosure.pdf","https://public.courts.alaska.gov/web/forms/docs/dr-2total.pdf")],
        "Arizona": [("AZ_financial_affidavit.pdf","https://www.azcourts.gov/Portals/0/31/Forms/AOCDR45H.pdf")],
        "Arkansas": [("AR_financial_affidavit.pdf","https://www.arcourts.gov/sites/default/files/FinancialAffidavit.pdf")],
        "California": [("CA_FL150_income_expense.pdf","https://www.courts.ca.gov/documents/fl150.pdf"),("CA_FL157_spousal_support.pdf","https://www.courts.ca.gov/documents/fl157.pdf")],
        "Colorado": [("CO_JDF1104_financial.pdf","https://www.courts.state.co.us/userfiles/file/Court_Probation/Self_Help/Forms/Family_Law/JDF%201104%20R7-20%20Sworn%20Financial%20Statement.pdf")],
        "Connecticut": [("CT_FM75_financial.pdf","https://www.jud.ct.gov/webforms/forms/fm075.pdf")],
        "Delaware": [("DE_financial_report.pdf","https://courts.delaware.gov/forms/download.aspx?id=39360")],
        "Florida": [("FL_12902b_short.pdf","https://www.flcourts.gov/content/download/405439/file/12.902(b)(1).pdf"),("FL_12902b2_long.pdf","https://www.flcourts.gov/content/download/405440/file/12.902(b)(2).pdf")],
        "Georgia": [("GA_financial_affidavit.pdf","https://georgiacourts.gov/wp-content/uploads/2020/11/Domestic-Relations-Financial-Affidavit.pdf")],
        "Hawaii": [("HI_financial_statement.pdf","https://www.courts.state.hi.us/docs/form/famcrt/1F-P-928.pdf")],
        "Idaho": [("ID_financial_statement.pdf","https://isc.idaho.gov/forms-repository/CAO%20FLP%201-7.pdf")],
        "Illinois": [("IL_financial_affidavit.pdf","https://www.illinoiscourts.gov/resources/a3c65b9b-eef1-4a2c-9d50-5df3c8b5d8d1/file")],
        "Indiana": [("IN_financial_declaration.pdf","https://www.in.gov/courts/files/financial-declaration.pdf")],
        "Iowa": [("IA_financial_affidavit.pdf","https://www.iowacourts.gov/media/cms/Financial_Affidavit_1D1A5C9B45A20.pdf")],
        "Kansas": [("KS_financial_affidavit.pdf","https://www.kscourts.org/KSCourts/media/KsCourts/Forms/Divorce/Financial-Affidavit.pdf")],
        "Kentucky": [("KY_financial_disclosure.pdf","https://kycourts.gov/Legal-Help/Documents/Financial%20Disclosure%20Statement.pdf")],
        "Louisiana": [("LA_financial_statement.pdf","https://www.lasc.org/rules/dist.ct/FinancialStatement.pdf")],
        "Maine": [("ME_financial_statement.pdf","https://www.courts.maine.gov/fees_forms/forms/FM-financial-statement.pdf")],
        "Maryland": [("MD_financial_statement.pdf","https://www.courts.state.md.us/sites/default/files/import/family/forms/ccdr030.pdf")],
        "Massachusetts": [("MA_financial_statement.pdf","https://www.mass.gov/doc/financial-statement-short-form-cjd301s/download")],
        "Michigan": [("MI_FOC23_support.pdf","https://courts.michigan.gov/Administration/SCAO/Forms/courtforms/foc23.pdf")],
        "Minnesota": [("MN_financial_disclosure.pdf","https://www.mncourts.gov/mncourtsgov/media/CourtForms/FAM111.pdf")],
        "Mississippi": [("MS_financial_statement.pdf","https://courts.ms.gov/research/forms/chancery/FinancialStatement.pdf")],
        "Missouri": [("MO_financial_statement.pdf","https://www.courts.mo.gov/file.jsp?id=3310")],
        "Montana": [("MT_financial_affidavit.pdf","https://courts.mt.gov/Portals/189/forms/family/financial_affidavit.pdf")],
        "Nebraska": [("NE_financial_affidavit.pdf","https://supremecourt.nebraska.gov/sites/default/files/CH6-12.pdf")],
        "Nevada": [("NV_financial_disclosure.pdf","https://www.nevadajudiciary.us/images/CommitteeMaterials/FamilyLaw/forms/Financial-Disclosure-Form.pdf")],
        "New Hampshire": [("NH_financial_affidavit.pdf","https://www.courts.nh.gov/sites/g/files/ehbemt471/files/documents/2020-12/nhjb-2065-dfe.pdf")],
        "New Jersey": [("NJ_CIS_financial.pdf","https://www.njcourts.gov/forms/10144_cis.pdf")],
        "New Mexico": [("NM_financial_disclosure.pdf","https://nmcourts.gov/wp-content/uploads/2022/08/4A-212.pdf")],
        "New York": [("NY_net_worth.pdf","https://www.nycourts.gov/forms/matrimonial/networth.pdf")],
        "North Carolina": [("NC_financial_affidavit.pdf","https://www.nccourts.gov/assets/inline-files/Family-Law-Financial-Affidavit-AOC-CV-613.pdf")],
        "North Dakota": [("ND_financial_statement.pdf","https://www.ndcourts.gov/Media/Default/Legal%20Self%20Help/Family%20Law/Financial_Statement.pdf")],
        "Ohio": [("OH_financial_disclosure.pdf","https://www.supremecourt.ohio.gov/JCS/CFC/Resources/Forms/divorce_dissolution/financial_disclosure.pdf")],
        "Oklahoma": [("OK_financial_statement.pdf","https://www.oscn.net/static/oscn/content/rules/forms/financial_statement.pdf")],
        "Oregon": [("OR_financial_declaration.pdf","https://www.courts.oregon.gov/forms/Documents/DR325.pdf")],
        "Pennsylvania": [("PA_income_expense.pdf","https://www.pacourts.us/assets/files/setting-5571/file-5644.pdf")],
        "Rhode Island": [("RI_financial_statement.pdf","https://www.courts.ri.gov/PublicResources/forms/Family%20Court%20Forms/Financial%20Statement.pdf")],
        "South Carolina": [("SC_financial_declaration.pdf","https://www.sccourts.org/forms/pdf/SCCA400.pdf")],
        "South Dakota": [("SD_financial_affidavit.pdf","https://ujs.sd.gov/uploads/forms/UJS-009.pdf")],
        "Tennessee": [("TN_income_affidavit.pdf","https://www.tncourts.gov/sites/default/files/docs/income_and_expense_statement.pdf")],
        "Texas": [("TX_inventory.pdf","https://www.txcourts.gov/media/1446862/inventory-and-appraisement.pdf")],
        "Utah": [("UT_financial_declaration.pdf","https://www.utcourts.gov/howto/divorce/docs/1112fa.pdf")],
        "Vermont": [("VT_financial_affidavit.pdf","https://www.vermontjudiciary.org/sites/default/files/documents/100-00270_Financial_Affidavit_fillable.pdf")],
        "Virginia": [("VA_financial_statement.pdf","https://www.courts.state.va.us/forms/circuit/cc1418.pdf")],
        "Washington": [("WA_financial_declaration.pdf","https://www.courts.wa.gov/forms/documents/DR01_0550_FinDeclaration.pdf")],
        "West Virginia": [("WV_financial_statement.pdf","https://www.courtswv.gov/public-resources/court-forms/family-court/SFF-Financial-Statement.pdf")],
        "Wisconsin": [("WI_FA4139_financial.pdf","https://www.wicourts.gov/formdisplay/FA-4139.pdf")],
        "Wyoming": [("WY_financial_affidavit.pdf","https://www.courts.state.wy.us/wp-content/uploads/2017/07/Financial-Affidavit.pdf")],
        "Washington DC": [("DC_financial_statement.pdf","https://www.dccourts.gov/sites/default/files/2021-12/Financial-Statement.pdf")],
    },
}


def get_forms_for_session(state: str, has_children: bool, wants_name_change: bool, has_assets: bool) -> dict:
    """
    Returns the exact subset of forms needed for a user's session.
    Keys are feature names, values are list of (filename, url) tuples.
    """
    needed = {}

    # Feature 1 — always needed
    needed["01_divorce"] = FORM_REGISTRY["01_divorce"].get(state, [])

    # Feature 2 — only if name change requested
    if wants_name_change:
        needed["02_name_change"] = (
            FORM_REGISTRY["02_name_change"].get("_FEDERAL", []) +
            FORM_REGISTRY["02_name_change"].get(state, [])
        )

    # Feature 3 — only if assets exist
    if has_assets:
        needed["03_asset"] = (
            FORM_REGISTRY["03_asset"].get("_FEDERAL", []) +
            FORM_REGISTRY["03_asset"].get(state, [])
        )

    # Feature 4 — only if children
    if has_children:
        needed["04_coparenting"] = FORM_REGISTRY["04_coparenting"].get(state, [])

    # Feature 5 — always needed (federal forms + state)
    needed["05_financial"] = (
        FORM_REGISTRY["05_financial"].get("_FEDERAL", []) +
        FORM_REGISTRY["05_financial"].get(state, [])
    )

    return needed
