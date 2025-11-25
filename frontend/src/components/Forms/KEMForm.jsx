import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { submitKEMForm, getKEMHistory } from '../../services/api';
import DateTimePicker from '../Common/DateTimePicker';
import FileUpload from '../Common/FileUpload';
import MultiSelect from '../Common/MultiSelect';
import GridSelector from '../Grid/GridSelector';
import HistoryTable from '../History/HistoryTable';
import DownloadButton from '../History/DownloadButton';
import './Form.css';

const KEMForm = () => {
  const [formData, setFormData] = useState({
    date_time: '',
    lot_number: '',
    item_type: '',
    erst_machine_no: '',
    mc_machine_no: '',
    cut_operator_payroll: '',
    ng_block_lot: '',
    ng_chip_qty_lot: '',
    block_number: '',
    confirm_date: '',
    reason: [],
    defects: [],
    judgement: 'Good',
    shifting_amount: '',
    shifting_direction: [],
    quality_case: 'open',
    process_selection: [],
    grid: Array(3).fill(null).map(() => Array(3).fill(false))
  });

  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [errors, setErrors] = useState({});

  const reasonOptions = ['After Repair', 'After Shut Down', 'Change item', 'Others'];
  const defectOptions = [
    'w shift', 'L shift', 'Sheet NG', 'W out/ Lout', 'Deformed', 'Slant Cut',
    'Pattern dent', 'Smearing', 'Partial print', 'Blunt cut', 'Others',
    'Rough cut', 'VP dent', 'Step Shift', 'Ridge/Dent'
  ];
  const directionOptions = ['W shift front', 'W shift back', 'L shift right', 'L shift left', 'Sheet NG', 'good'];
  const processOptions = ['Stacking Feedback', 'Cutting Feedback'];

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await getKEMHistory();
      setHistory(response.data);
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.date_time) newErrors.date_time = 'Required';
    if (!formData.lot_number || formData.lot_number.length > 10) {
      newErrors.lot_number = 'Required (max 10 characters)';
    }
    if (!formData.item_type) newErrors.item_type = 'Required';
    if (!formData.erst_machine_no) newErrors.erst_machine_no = 'Required';
    if (!formData.mc_machine_no) newErrors.mc_machine_no = 'Required';
    if (!formData.cut_operator_payroll) newErrors.cut_operator_payroll = 'Required';
    if (!formData.ng_block_lot) newErrors.ng_block_lot = 'Required';
    if (!formData.ng_chip_qty_lot) newErrors.ng_chip_qty_lot = 'Required';
    if (!formData.block_number) newErrors.block_number = 'Required';
    if (!formData.confirm_date) newErrors.confirm_date = 'Required';
    if (formData.reason.length === 0) newErrors.reason = 'Required';
    if (formData.defects.length === 0) newErrors.defects = 'Required';
    if (!formData.shifting_amount) newErrors.shifting_amount = 'Required';
    if (formData.shifting_direction.length === 0) newErrors.shifting_direction = 'Required';
    if (formData.process_selection.length === 0) newErrors.process_selection = 'Required';
    if (files.length === 0) newErrors.files = 'At least one photo is required';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      toast.error('Please fill all required fields');
      return;
    }

    setLoading(true);
    try {
      const formDataToSend = new FormData();
      
      Object.keys(formData).forEach(key => {
        if (key === 'grid') {
          formDataToSend.append(key, JSON.stringify(formData[key]));
        } else if (Array.isArray(formData[key])) {
          formDataToSend.append(key, JSON.stringify(formData[key]));
        } else {
          formDataToSend.append(key, formData[key]);
        }
      });

      files.forEach(file => {
        formDataToSend.append('photos', file);
      });

      await submitKEMForm(formDataToSend);
      toast.success('Form submitted successfully!');
      
      handleClear();
      loadHistory();
    } catch (error) {
      toast.error(error.message || 'Failed to submit form');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setFormData({
      date_time: '',
      lot_number: '',
      item_type: '',
      erst_machine_no: '',
      mc_machine_no: '',
      cut_operator_payroll: '',
      ng_block_lot: '',
      ng_chip_qty_lot: '',
      block_number: '',
      confirm_date: '',
      reason: [],
      defects: [],
      judgement: 'Good',
      shifting_amount: '',
      shifting_direction: [],
      quality_case: 'open',
      process_selection: [],
      grid: Array(3).fill(null).map(() => Array(3).fill(false))
    });
    setFiles([]);
    setErrors({});
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <h2 className="form-title">B1 KEM Cutting Process Feedback</h2>
          
          <div className="form-row">
            <div className="form-group">
              <DateTimePicker
                label="Date and Time"
                value={formData.date_time}
                onChange={(value) => handleChange('date_time', value)}
                error={errors.date_time}
              />
            </div>
            <div className="form-group">
              <label>Lot Number (max 10 chars)</label>
              <input
                type="text"
                value={formData.lot_number}
                onChange={(e) => handleChange('lot_number', e.target.value)}
                maxLength={10}
                className={errors.lot_number ? 'error' : ''}
              />
              {errors.lot_number && <div className="error-message">{errors.lot_number}</div>}
            </div>
            <div className="form-group">
              <label>Item Type</label>
              <input
                type="text"
                value={formData.item_type}
                onChange={(e) => handleChange('item_type', e.target.value)}
                className={errors.item_type ? 'error' : ''}
              />
              {errors.item_type && <div className="error-message">{errors.item_type}</div>}
            </div>
            <div className="form-group">
              <label>ERST Machine No</label>
              <input
                type="text"
                value={formData.erst_machine_no}
                onChange={(e) => handleChange('erst_machine_no', e.target.value)}
                className={errors.erst_machine_no ? 'error' : ''}
              />
              {errors.erst_machine_no && <div className="error-message">{errors.erst_machine_no}</div>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group mc-machine-no">
              <label>MC Machine No</label>
              <input
                type="text"
                value={formData.mc_machine_no}
                onChange={(e) => handleChange('mc_machine_no', e.target.value)}
                className={errors.mc_machine_no ? 'error' : ''}
              />
              {errors.mc_machine_no && <div className="error-message">{errors.mc_machine_no}</div>}
            </div>
            <div className="form-group">
              <label>Cut Operator Payroll</label>
              <input
                type="text"
                value={formData.cut_operator_payroll}
                onChange={(e) => handleChange('cut_operator_payroll', e.target.value)}
                className={errors.cut_operator_payroll ? 'error' : ''}
              />
              {errors.cut_operator_payroll && <div className="error-message">{errors.cut_operator_payroll}</div>}
            </div>
            <div className="form-group">
              <label>NG Block/Lot</label>
              <input
                type="text"
                value={formData.ng_block_lot}
                onChange={(e) => handleChange('ng_block_lot', e.target.value)}
                className={errors.ng_block_lot ? 'error' : ''}
              />
              {errors.ng_block_lot && <div className="error-message">{errors.ng_block_lot}</div>}
            </div>
            <div className="form-group">
              <label>NG chip Qty/Lot(pcs)</label>
              <input
                type="text"
                value={formData.ng_chip_qty_lot}
                onChange={(e) => handleChange('ng_chip_qty_lot', e.target.value)}
                className={errors.ng_chip_qty_lot ? 'error' : ''}
              />
              {errors.ng_chip_qty_lot && <div className="error-message">{errors.ng_chip_qty_lot}</div>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Block Number</label>
              <input
                type="text"
                value={formData.block_number}
                onChange={(e) => handleChange('block_number', e.target.value)}
                className={errors.block_number ? 'error' : ''}
              />
              {errors.block_number && <div className="error-message">{errors.block_number}</div>}
            </div>
            <div className="form-group">
              <label>Confirm Date</label>
              <input
                type="date"
                value={formData.confirm_date}
                onChange={(e) => handleChange('confirm_date', e.target.value)}
                className={errors.confirm_date ? 'error' : ''}
              />
              {errors.confirm_date && <div className="error-message">{errors.confirm_date}</div>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <MultiSelect
                label="Reason"
                options={reasonOptions}
                value={formData.reason}
                onChange={(value) => handleChange('reason', value)}
                error={errors.reason}
              />
            </div>
            <div className="form-group">
              <MultiSelect
                label="Defect Name"
                options={defectOptions}
                value={formData.defects}
                onChange={(value) => handleChange('defects', value)}
                error={errors.defects}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Judgement</label>
              <select
                value={formData.judgement}
                onChange={(e) => handleChange('judgement', e.target.value)}
                style={{ color: formData.judgement === 'Good' ? 'green' : 'red' }}
              >
                <option value="Good">Good</option>
                <option value="NG">NG</option>
              </select>
            </div>
            <div className="form-group">
              <label>Shifting Amount (micron)</label>
              <input
                type="text"
                value={formData.shifting_amount}
                onChange={(e) => handleChange('shifting_amount', e.target.value)}
                className={errors.shifting_amount ? 'error' : ''}
              />
              {errors.shifting_amount && <div className="error-message">{errors.shifting_amount}</div>}
            </div>
            <div className="form-group">
              <MultiSelect
                label="Shifting Direction"
                options={directionOptions}
                value={formData.shifting_direction}
                onChange={(value) => handleChange('shifting_direction', value)}
                error={errors.shifting_direction}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Quality Case</label>
              <select
                value={formData.quality_case}
                onChange={(e) => handleChange('quality_case', e.target.value)}
              >
                <option value="open">open</option>
                <option value="close">close</option>
              </select>
            </div>
            <div className="form-group">
              <MultiSelect
                label="Process Selection"
                options={processOptions}
                value={formData.process_selection}
                onChange={(value) => handleChange('process_selection', value)}
                error={errors.process_selection}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <GridSelector
                size={3}
                value={formData.grid}
                onChange={(grid) => handleChange('grid', grid)}
                label="ERST MACHINE BACKSIDE / FRONT SIDE"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <FileUpload
                files={files}
                onChange={setFiles}
                error={errors.files}
              />
            </div>
          </div>

          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={handleClear}>
              Clear
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? (
                <>
                  <span className="loading-spinner"></span>
                  Submitting...
                </>
              ) : (
                'Send Email'
              )}
            </button>
          </div>
        </div>
      </form>

      <div className="form-section">
        <h2 className="form-title">Summary History</h2>
        <HistoryTable data={history} />
        <DownloadButton formType="kem" />
      </div>
    </div>
  );
};

export default KEMForm;

